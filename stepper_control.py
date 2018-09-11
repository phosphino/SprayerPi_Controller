import RPi.GPIO as GPIO
from time import sleep
from timeit import default_timer as timer
import statistics as st

class motorcontrol:
	def __init__(self):
		self.__DIR = 38
		self.__STEP = 40
		self.__front_switch = 36
		self.__back_switch = 32
		self.__front_dir = 1
		self.__back_dir = 0	
		self.__microstep_map = {1: (0,0,0), 2: (1,0,0), 4 : (0,1,0), 8:(1,1,0), 16:(0,0,1),	32: (0,1,1)}
		self.__microstep_keys = [1, 2, 4, 8, 16, 32]
		self.__microstepping = (18,16,12)#Board numbers for microstepping pins
		self.__current_microstep = None
		self.__current_dir = None
		self.__current_set_speed = 0
		
		self.__go_sentinal = False		
		self.__delay = 0.0005
		self.__track_width = None
		self.__inches_per_step = None
		self.__spray_width = 2.5
	
		GPIO.setmode(GPIO.BOARD)
	
		GPIO.setup([self.__STEP, self.__DIR], GPIO.OUT)
		GPIO.setup([self.__front_switch, self.__back_switch], GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(self.__microstepping, GPIO.OUT)
		
		#For Single Stepping Endstop Detection
		GPIO.add_event_detect(self.__front_switch, GPIO.FALLING, bouncetime = 60, callback = self.front_endstop)
		GPIO.add_event_detect(self.__back_switch, GPIO.FALLING, bouncetime = 60, callback = self.back_endstop)
			
		self.set_dir(self.__back_dir)	
		self.initialize_track()	
		
	def initialize_track(self):
		self.set_microstepping(4)
		self.calibrate_settings()
		
	def calibrate_settings(self, trials = 10):
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
		self.__track_width = int(st.mean(width))
		self.__inches_per_step = 5.00 / self.__track_width
		self.calculate_speed()
		
	
	def set_speed(self, speed):
		new_delay = (self.__inches_per_step / speed) / 2.00
		self.set_delay(new_delay)		
		
	def get_speed(self):
		return self.__current_set_speed
		
	def calculate_speed(self):
		self.__current_set_speed = self.__inches_per_step / (self.__delay * 2.00)
	
	def go_to_midpoint(self):
		self.go_to_endstop()
		half_width = int (self.__track_width / 2)
		self.counted_steps(half_width)		
	
	def oscillate_current_position(self, width = 2.5, cycles = 10):
		total_steps = int( width / self.__inches_per_step )
		half_steps = int(total_steps / 2)
		self.set_dir(self.__back_dir)
		for i in range(cycles):
			self.counted_steps(half_steps)
			self.reverse_dir()
			self.counted_steps(total_steps)
			self.reverse_dir()
			self.counted_steps(half_steps)
					
	def set_spray_width(self, width):
		self.__spray_width = width
	
	def get_spray_width(self):
		return self.__spray_width
		
	def set_dir(self, direction):
		GPIO.output(self.__DIR, direction)
		self.__current_dir = direction
	
	def get_dir(self):
		return self.__current_dir
		
	def check_dir(self):
		state = self.get_endstop_state()
		if state[0] == 0:
			self.set_dir(self.__back_dir)
		if state[1] == 0:
			self.set_dir(self.__front_dir)	
			
	def reverse_dir(self):
		if self.__current_dir == self.__front_dir:
			self.set_dir(self.__back_dir)
		else:
			self.set_dir(self.__front_dir)
	
	def set_delay(self, delay):
		self.__delay = delay
		self.calculate_speed()
	
	def get_delay(self):
		return self.__delay
		
	def get_endstop_state(self):
		return [int(GPIO.input(self.__front_switch)), int(GPIO.input(self.__back_switch))]
		
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
		GPIO.output(self.__microstepping, self.__microstep_map[key])
		self.__current_microstep = key
		
	def get_microstepping(self):
		return self.__current_microstep
	
	def single_step(self):
		GPIO.output(self.__STEP, 1)
		sleep(self.__delay)
		GPIO.output(self.__STEP, 0)
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
