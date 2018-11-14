import RPi.GPIO as GPIO
from time import sleep
from timeit import default_timer as timer
import statistics as st
from syringe_control import syringecontrol
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import shelve

#BOARD PIN #'S FOR RPI 3
DIR = 38
STEP = 40
ENABLE = 33

front_switch = 36
back_switch = 32

microstepping = (18,16,12)#Board numbers for microstepping pins

gas_solenoid = 37
ultrasonic_switch = 35

front_dir = 0
back_dir = 1
microstep_map = {0 : (0,0,0), 1 : (1,0,0), 2 : (0,1,0), 3 :(1,1,0), 4 :(0,0,1), 5 : (0,1,1)}

gas_solenoid = 37
ultrasonic_switch = 35

class spraycontrol(QObject):
	operation_done = pyqtSignal(bool)
	sweep_complete = pyqtSignal()
	def __init__(self):
		QObject.__init__(self)
		
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		
		GPIO.setup([STEP, DIR, ENABLE], GPIO.OUT)
		GPIO.setup([front_switch, back_switch], GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(microstepping, GPIO.OUT)
		
		#For Single Stepping Endstop Detection
		GPIO.add_event_detect(front_switch, GPIO.FALLING, callback = self.front_endstop)
		GPIO.add_event_detect(back_switch, GPIO.FALLING, callback = self.back_endstop)
		
		self.syringePump = syringecontrol()
		
		GPIO.setup(gas_solenoid, GPIO.OUT)
		GPIO.setup(ultrasonic_switch, GPIO.OUT)
		
		self.__operation_mode = None
		self.__go_sentinal = False
		self.__travel_delay = 0.001
		self.__travel_microstepping = 0
		
		self.__track_width_steps = None
		self.__track_width_inches = None
		self.__inches_per_step = None
		self.__delay = 0.001
		self.__current_dir = None
		self.__pause_time = 0
		self.__spray_width_inches = None
		self.__current_microstep = None
		self.__spray_cycle_motor_parameters = {}
		self.__traverse_params = []
		
		self.set_dir(0)
		self.set_microstepping(0)
		GPIO.output(ENABLE, 1)
		with shelve.open('stepper_calibration' , 'r') as shelf:
			try:
				self.set_inches_per_step(float(shelf['inches_per_step']))		
				self.set_track_width_steps(float(shelf['track_width_steps']))
				print('saving to shelf', shelf['inches_per_step'])
				print('saving to shelf', shelf['track_width_steps'])
			except:
				pass
			
	def pneumatic_ON(self):
		GPIO.output(gas_solenoid, 1)
		
	def pneumatic_OFF(self):
		GPIO.output(gas_solenoid, 0)
			
	def set_syringeSettings(self, volume = 0.00, vol_units = 0, rate = 0.0, rate_units = 0):
		self.syringePump.set_dispense_volume(volume, units = vol_units)
		self.syringePump.set_rate(rate, units = rate_units)
	
	def set_sprayParameters(self, params):
		self.__spray_cycle_motor_parameters = params
			
	def set_operationMode(self, mode):
		self.__operation_mode = mode
		
	def set_traverseParameters(self, delay, microstepping):
		self.__traverse_params = [delay, microstepping]
		
	def perform_operation(self):
		if self.__operation_mode == 0:
			self.calibrate_inchesperstep()
		if self.__operation_mode == 1:
			self.spray_cycle_motor(**self.__spray_cycle_motor_parameters)
		if self.__operation_mode == 2:
			self.traverse(*self.__traverse_params)
		if self.__operation_mode == 3:
			self.go_to_midpoint()
	
	def traverse(self, delay, microstepping):
		current_delay = self.get_delay()
		current_microstepping = self.get_microstepping()
		self.set_delay(delay)
		self.set_microstepping(microstepping)
		if 0 not in self.get_endstop_state():
			self.__go_sentinal = True
			while self.__go_sentinal:
				self.single_step()
		self.check_dir()
		self.__go_sentinal = True
		while self.__go_sentinal:
			self.single_step()
		self.set_delay(current_delay)
		self.set_microstepping(current_microstepping)
		self.check_dir()
		self.operation_done.emit(True)
		
	def go_to_midpoint(self):
		current_delay = self.get_delay()
		current_microstepping = self.get_microstepping()
		self.set_delay(self.__travel_delay)
		self.set_microstepping(self.__travel_microstepping)
		if 0 not in self.get_endstop_state():
			self.__go_sentinal = True
			while self.__go_sentinal:
				self.single_step()
		self.check_dir()
		midpoint_steps = int(self.__track_width_steps / 2)
		self.__go_sentinal = True
		for i in range(midpoint_steps):
			if self.__go_sentinal:
				self.single_step()
		self.__go_sentinal = False
		self.set_delay(current_delay)
		self.set_microstepping(current_microstepping)
		self.operation_done.emit(True)
		
	def calibrate_inchesperstep(self, sweeps = 10):
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

		for i in range(sweeps):
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
		self.operation_done.emit(True)
		
		with shelve.open('stepper_calibration' , 'w') as shelf:
			shelf['inches_per_step'] = self.__track_width_inches
			shelf['track_width_steps'] = self.__track_width_steps
			print('saving to shelf ', shelf['inches_per_step'])
			print('saving to shelf', shelf['track_width_steps'])
			
		return [self.__inches_per_step, self.__track_width_steps]
		
	def spray_cycle_motor(self, delay = 0.001, pause_time = 0, microstepping = 0, width = 0, mode = 0):
		self.syringePump.clear_volume_dispensed()
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
				
		spray_width_steps = int(width / self.__inches_per_step)
		half_spray_width_steps = int(spray_width_steps/2)		
		
		for i in range(half_spray_width_steps):
			if self.__go_sentinal == False:
				break
			self.single_step()
			
		self.set_delay(delay)
		self.set_microstepping(microstepping)
		factor = 2**self.get_microstepping()
		spray_width_steps = spray_width_steps * factor			
		self.reverse_dir()
		target_dispense_volume = float(self.syringePump.get_dispense_volume()[0])
		volume_dispensed = 0.0

		while volume_dispensed < target_dispense_volume:
			print('volume dispensed: ', volume_dispensed)
			self.pneumatic_ON()
			self.syringePump.run_pump()		
			for i in range(spray_width_steps):
				if self.__go_sentinal == False:
					break
				self.single_step()
			self.reverse_dir()
			volume_dispensed = float(self.syringePump.get_volume_dispensed()[0])
			self.sweep_complete.emit()
			if self.__pause_time > 0:
				print('pausing')
				self.pneumatic_OFF()
				self.syringePump.stop_pump()
				sleep(self.__pause_time)
		
		self.pneumatic_OFF()

		self.operation_done.emit(True)
	
	def set_pause_time(self, pause_time):
		self.__pause_time = pause_time
		
	def set_spray_width(self, spray_width):
		self.__spray_width_inches = spray_width
		
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
		print("Hit Front EndSTOP", self.__go_sentinal)
	
	def back_endstop(self, channel):
		if 0 not in self.get_endstop_state():
			return
		self.__go_sentinal = False
		print("Hit Back EndSTOP", self.__go_sentinal)
		
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
	
