import RPi.GPIO as GPIO
from time import sleep
from timeit import default_timer as timer
import statistics as st
from stepper_control import motorcontrol
from syringe_control import syringecontrol

gas_solenoid = 37
ultrasonic_switch = 35

class spraycontrol(motorcontrol):
	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		super().__init__()
		
		GPIO.setup(gas_solenoid, GPIO.OUT)
		GPIO.setup(ultrasonic_switch, GPIO.OUT)
		
			
