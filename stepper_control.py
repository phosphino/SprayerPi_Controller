import RPi.GPIO as GPIO
from time import sleep
from timeit import default_timer as timer
import statistics as st
from PyQt5.QtCore import QObject, pyqtSignal

#BOARD PIN #'S FOR RPI 3
DIR = 38
STEP = 40
ENABLE = 33

front_switch = 36
back_switch = 32

microstepping = (18,16,12)#Board numbers for microstepping pins

gas_solenoid = 37
ultrasonic_switch = 35

front_dir = 1
back_dir = 0
microstep_map = {0 : (0,0,0), 1 : (1,0,0), 2 : (0,1,0), 3 :(1,1,0), 4 :(0,0,1), 5 : (0,1,1)}

class motorcontrol(QObject):
	sweep_complete = pyqtSignal()
	def __init__(self):
		QObject.__init__(self)
		self.__current_microstep = None
		self.__current_dir = None
		self.__current_set_speed = 0
		
		self.__track_width_inches = 4.764 #Track length in inches
		self.__go_sentinal = False #sentinal for moving motor
		self.__delay = 0.001 #delay between step pulses
		self.__travel_delay = 0.001
		self.__travel_microstepping = 0
		self.__track_width_steps = None#Steps to cross track
		self.__inches_per_step = None#how many inches traveled per step 
		self.__pause_time = None #pause time during spray cycle
		self.__spray_width_inches = None #how many inches to spray
		self.__cycleNumber = None
		
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
	
		GPIO.setup([STEP, DIR, ENABLE], GPIO.OUT)
		GPIO.setup([front_switch, back_switch], GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(microstepping, GPIO.OUT)
		
		#For Single Stepping Endstop Detection
		GPIO.add_event_detect(front_switch, GPIO.FALLING, callback = self.front_endstop)
		GPIO.add_event_detect(back_switch, GPIO.FALLING, callback = self.back_endstop)
			
		self.set_dir(back_dir)	
		self.initialize_track()	
		
	def calibrate_inchesperstep(self):
		current_delay = self.get_delay()
		current_microstepping = self.get_microstepping()
		self.set_delay(self.__travel_delay)
		self.set_microstepping(self.__travel_microstepping)
		width = []
		self.check_dir()
		if 0 not in self.get_endstop_state():
			self.__go_sentinal = True
			while self.__go_sentinal:
				self.single_step()
			self.check_dir()
		for i in range(10):
			count = 0
			self.__go_sentinal = True
			while self.__go_sentinal:
				self.single_step()
				count += 1
			width.append(count)
			self.check_dir()
		mean_width = int(st.mean(width))
		self.__track_width_steps = mean_width
		self.__inches_per_step = self.__track_width_inches / float(mean_width)
		
		self.set_delay(current_delay)
		self.set_microstepping(current_microstepping)
		
		return [self.__inches_per_step, self.__track_width_steps]
		
	def spray_cycle_motor(self):
		current_delay = self.get_delay()
		current_microstepping = self.get_microstepping()
		self.set_delay(self.__travel_delay)
		self.set_microstepping(self.__travel_microstepping)
		if 0 not in self.get_endstop_state():
			self.__go_sentinal = True
			while self.__go_sentinal:
				self.single_step()
		self.check_dir()
		half_width = int(self.__track_width_steps / 2)
		self.__go_sentinal = True			
		for i in range(half_width):
			if self.__go_sentinal == False:
				break
			self.single_step()
				
		spray_width_steps = int(self.__spray_width_inches / self.__inches_per_step)
		half_spray_width_steps = int(spray_width_steps/2)		
		
		for i in range(half_spray_width_steps):
			if self.__go_sentinal == False:
				break
			self.single_step()
			
		self.set_delay(current_delay)
		self.set_microstepping(current_microstepping)
		factor = 2**current_microstepping
		print(factor)
		spray_width_steps = spray_width_steps * factor			
		self.reverse_dir()
		sweeps = int(self.__cycleNumber * 2)
		for i in range(sweeps):
			
			for i in range(spray_width_steps):
				if self.__go_sentinal == False:
					break
				self.single_step()
			self.reverse_dir()
			self.sweep_complete.emit()
			if self.__pause_time > 0:
				sleep(self.__pause_time)
	
	

	
	def set_pause_time(self, pause_time):
		self.__pause_time = pause_time
		
	def set_spray_width(self, spray_width):
		self.__spray_width_inches = spray_width
		
	def set_cycle_number(self, cycles):
		self.__cycleNumber = cycles
		
	def initialize_track(self):
		self.set_microstepping(0)
		GPIO.output(ENABLE, 1)
		#self.calibrate_settings()
		
	def set_track_width_inches(self, width):
		self.__track_width_inches = width
	
	def get_track_width_inches(self):
		return self.__track_width_inches
		
	def set_track_width_steps(self, width):
		self.__track_width_steps = width
		
	def get_track_width_steps(self):
		return self.__track_width_steps
		
	def set_inches_per_step(self, inches_per_step):
		self.__inches_per_step = inches_per_step
	
	def set_dir(self, direction):
		GPIO.output(DIR, direction)
		self.__current_dir = direction
	
	def get_dir(self):
		return self.__current_dir
		
	def check_dir(self):
		state = self.get_endstop_state()
		if state[0] == 0:
			self.set_dir(back_dir)
		if state[1] == 0:
			self.set_dir(front_dir)	
			
	def reverse_dir(self):
		if self.__current_dir == front_dir:
			self.set_dir(back_dir)
		else:
			self.set_dir(front_dir)
	
	def set_delay(self, delay):
		self.__delay = delay
	
	def get_delay(self):
		return self.__delay
		
	def get_endstop_state(self):
		return [int(GPIO.input(front_switch)), int(GPIO.input(back_switch))]
		
	def front_endstop(self, channel):
		if 0 not in self.get_endstop_state():
			return
		self.__go_sentinal = False
		print("Hit Front EndSTOP")
	
	def back_endstop(self, channel):
		if 0 not in self.get_endstop_state():
			return
		self.__go_sentinal = False
		print("Hit Back EndSTOP")
		
	def set_microstepping(self, key):
		GPIO.output(microstepping, microstep_map[key])
		self.__current_microstep = key
		
	def get_microstepping(self):
		return self.__current_microstep
	
	def single_step(self):
		GPIO.output(STEP, 1)
		sleep(self.__delay)
		GPIO.output(STEP, 0)
		sleep(self.__delay)
					
	def cleanup(self):
		GPIO.cleanup()
