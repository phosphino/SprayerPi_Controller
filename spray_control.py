import RPi.GPIO as GPIO
from time import sleep
from timeit import default_timer as timer
import statistics as st
from stepper_control import motorcontrol
from syringe_control import syringecontrol
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

gas_solenoid = 37
ultrasonic_switch = 35

class spraycontrol(QObject):
	def __init__(self):
		QObject.__init__(self)
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		self.stepper = motorcontrol()
		self.syringePump = syringecontrol()
		
		GPIO.setup(gas_solenoid, GPIO.OUT)
		GPIO.setup(ultrasonic_switch, GPIO.OUT)
		
		self.__selectedSpray_mode = None
		
		
	def setMotor_settings(self, motor_delay, microstepping, track_length):
		
		
	def setSpray_settings(self, spraymode, volume, vol_units, dispense_rate,
							dispense_units, pause_time, spray_width):
		
		
		self.__selectedSpray_mode = spraymode
			
