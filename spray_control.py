import RPi.GPIO as GPIO
from time import sleep
from timeit import default_timer as timer
import statistics as st
from stepper_control import motorcontrol
from syringe_control import syringecontrol
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import shelve

gas_solenoid = 37
ultrasonic_switch = 35

class spraycontrol(QObject):
	operation_done = pyqtSignal(bool)
	motor_sweep_complete = pyqtSignal()
	def __init__(self):
		QObject.__init__(self)
		
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		
		self.stepperMotor = motorcontrol()
		self.syringePump = syringecontrol()
		
		GPIO.setup(gas_solenoid, GPIO.OUT)
		GPIO.setup(ultrasonic_switch, GPIO.OUT)
		
		self.__operation_mode = None
		
		with shelve.open('stepper_INCHperSTEP_calibration' , 'r') as shelf:
			self.stepperMotor.set_inches_per_step(float(shelf['inches_per_step']))		
			self.stepperMotor.set_track_width_steps(float(shelf['track_width_steps']))
			
		self.__selectedSpray_mode = None
		self.stepperMotor.sweep_complete.connect(self.plot_update)
		
	def plot_update(self):
		self.motor_sweep_complete.emit()
		
	def set_operationMode(self, mode):
		self.__operation_mode = mode
		
	def perform_operation(self):
		if self.__operation_mode == 0:
			self.calibrateMotor_operation()
		if self.__operation_mode == 1:
			self.runSpray_operation()
		
	
	def calibrateMotor_operation(self):
		data = self.stepperMotor.calibrate_inchesperstep()
		with shelve.open('stepper_INCHperSTEP_calibration' , 'c') as shelf:
			shelf['inches_per_step'] = float(data[0])
			shelf['track_width_steps'] = float(data[1])
		self.operation_done.emit(True)
		
	def runSpray_operation(self):
		self.stepperMotor.spray_cycle_motor()	
		self.operation_done.emit(True)	
		

	def setMotor_settings(self, motor_delay, microstepping, track_length):
		self.stepperMotor.set_delay(motor_delay)
		self.stepperMotor.set_microstepping(microstepping)
		self.stepperMotor.set_track_width_inches(track_length)
				
	def setSpray_settings(self, spraymode, cycles, volume, vol_units, dispense_rate,
							dispense_units, pause_time, spray_width):
				
		self.__selectedSpray_mode = spraymode
		self.syringePump.set_rate(dispense_rate, units = dispense_units)
		self.syringePump.set_dispense_volume(volume, units = vol_units)
		self.stepperMotor.set_pause_time(pause_time)
		self.stepperMotor.set_spray_width(spray_width)
		self.stepperMotor.set_cycle_number(cycles)
	
