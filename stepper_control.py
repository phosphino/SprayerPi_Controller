import RPi.GPIO as GPIO
from time import sleep
from timeit import default_timer as timer
import statistics as st

#BOARD PIN #'S FOR RPI 3
DIR = 38
STEP = 40
ENABLE = 33
front_switch = 36
back_switch = 32
microstepping = (18,16,12)#Board numbers for microstepping pins

front_dir = 1
back_dir = 0	
microstep_map = {1: (0,0,0), 2: (1,0,0), 4 : (0,1,0), 8:(1,1,0), 16:(0,0,1), 32: (0,1,1)}

class motorcontrol:
	def __init__(self):
		self.__current_microstep = None
		self.__current_dir = None
		self.__current_set_speed = 0
		
		self.__go_sentinal = False
		self.__spray_sentinal = False		
		self.__delay = 0.0005
		self.__track_width = None
		self.__inches_per_step = None
		
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
	
		GPIO.setup([STEP, DIR, ENABLE], GPIO.OUT)
		GPIO.setup([front_switch, back_switch], GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(microstepping, GPIO.OUT)
		
		#For Single Stepping Endstop Detection
		GPIO.add_event_detect(front_switch, GPIO.FALLING, bouncetime = 60, callback = self.front_endstop)
		GPIO.add_event_detect(back_switch, GPIO.FALLING, bouncetime = 60, callback = self.back_endstop)
			
		self.set_dir(back_dir)	
		self.initialize_track()	
		
	def initialize_track(self):
		self.set_microstepping(4)
		GPIO.output(ENABLE, 1)
		#self.calibrate_settings()
		
	def calibrate_settings(self, trials = 3):
		factor = self.__current_microstep
		self.go_to_endstop()
		width = []
		for i in range(trials):
			self.check_dir()
			count = 0
			self.__go_sentinal = True
			while self.__go_sentinal:
				self.single_step()
				count = count + 1
			width.append(count)
		if trials > 1:
			self.__track_width = int(st.mean(width))
			self.__inches_per_step = 4.764 / self.__track_width

	def get_track_width(self):
		return self.__track_width
		
	def get_inches_per_step(self):
		return self.__inches_per_step
	
	def go_to_midpoint(self):
		self.go_to_endstop()
		half_width = int (self.__track_width / 2)
		self.counted_steps(half_width)		
	
	#FROM MIDPOINT, STEPS HALF-WIDTH THEN CYCLES FULL STEPS
	def spray_cycle_motor(self, width = 2.75, cycles = 200, spray_delay = 0):
		total_steps = int( width / self.__inches_per_step )
		half_steps = int(total_steps / 2)
		self.set_dir(back_dir)
		self.counted_steps(half_steps)
		self.reverse_dir()
		for i in range(cycles):
			start = timer()
			self.counted_steps(total_steps)
			self.reverse_dir()
			self.counted_steps(total_steps)
			self.reverse_dir()
			sleep(spray_delay)
			end = timer()
			speed = (2*width)/(end-start)
			print("Average Speed During Travel: ", speed,"inches/sec")
					
	def set_spray_width(self, width):
		self.__spray_width = width
	
	def get_spray_width(self):
		return self.__spray_width
		
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
		
	def counted_steps(self, steps):
		self.__go_sentinal = True
		while self.__go_sentinal:
			for i in range(steps):
				self.single_step()
				if self.__go_sentinal == False:
					break
			self.__go_sentinal = False
		
	def go_to_endstop(self):
		self.check_dir()
		if 0 in self.get_endstop_state():
			return
		self.__go_sentinal = True
		while self.__go_sentinal:
			self.single_step()
	
	def traverse(self):
		self.check_dir()
		self.__go_sentinal = True
		while self.__go_sentinal:
			self.single_step()
			
	def timed_traverse(self):
		self.go_to_endstop()
		start = timer()
		self.traverse()
		end = timer()
		return (end - start)
					
	def cleanup(self):
		GPIO.cleanup()
