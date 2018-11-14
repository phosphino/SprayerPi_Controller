from pyqtTemp import adatemp
import RPi.GPIO as GPIO
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, QEventLoop, QObject
import pyqtgraph as pg
import smbus
from time import sleep 

hotplate_relay = 11
BUS = 1
ADDRESS = 0x50#ADDRESS OF TPL0102 DIGITAL POTENTIOMETER WITH 256 TAPS
#THE DIGITAL POTENTIOMETER USED IS TEXAS INSTRUMENTS TPL0102 PUT IN A RHEOSTAT CONFIGURATION
REG_A = 0x00 #ADDRESS OF THE REGISTER WIPER 'A' ON THE TPL0102
REG_B = 0x01
#USING THE RHEOSTAT FOR PID CONTROL OF THE HEATING ELEMENT BY USE OF DIMMER FUNCTION ON HOTPLATE POWER SUPPLY

class thermocouplecontrol(QObject):
	temperature_data = pyqtSignal(float)

	def __init__(self):
		QObject.__init__(self)
		self.thermocouple = adatemp()
	
	def new_temp_emit(self):
		while True:
			current_temp = self.thermocouple.temp()
			self.temperature_data.emit(current_temp)
			sleep(1)


class hotplatecontrol(QObject):
	register_value = pyqtSignal(int)

	def __init__(self, p = 34.0, i = 2.0, d = 35):
		QObject.__init__(self)
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(hotplate_relay, GPIO.OUT)
		
		self.bus = smbus.SMBus(BUS)
		self.__heating_sentinal = False
		
		self.__kp = p
		self.__ki = i
		self.__kd = d
		
		self.__pvalue = 0
		self.__ivalue = 0
		self.__dvalue = 0
		
		self.__error = 0.0
		self.__setpoint = 0.0
		self.__integrator = 0.0
		self.__derivator = 0.0
		
		self.write_PID(0)

		
	def set_kp(self, p):
		self.__kp = p
		return self.__kp
		
	def get_kp(self):
		return self.__kp
		
	def set_ki(self, i):
		self.__ki = i
		return self.__ki
		
	def get_ki(self):
		return self.__ki
		
	def set_kd(self, d):
		self.__kd = d
		return self.__kd
		
	def get_kd(self):
		return self.__kd	
		
	#ACTIVATE THE RELAY WHICH TURNS ON THE HOTPLATE POWER SUPPLY
	#HOTPLATE POWER SUPPPLY IS PROVIDING CURRENT TO HEATING ELEMENT WHEN RELAY IS ACTIVATED
	#THE AMOUNT OF CURRENT IS DICTATED BY THE RESISTANCE PROVIDED BY THE RHEOSTAT
	def activate_relay(self):
		GPIO.output(hotplate_relay, GPIO.HIGH)
		return GPIO.input(hotplate_relay)
		
	def deactivate_relay(self):
		GPIO.output(hotplate_relay, GPIO.LOW)
		self.__heating_sentinal = False
		return GPIO.input(hotplate_relay)
		
	def query_relay(self):
		return GPIO.input(hotplate_relay)
		
	def setPoint_start(self, setpoint):
		self.__integrator = 0.0
		self.__derivator = 0.0
		self.__setpoint = setpoint
		self.__heating_sentinal = True
		#Dim Hotplate PowerSupply to zero
		self.write_PID(0)
		self.register_value.emit(0)
		#Turn on hotplate
		self.activate_relay()
	
	@pyqtSlot(float)	
	def calculatePID(self, current_temp):
		if self.__heating_sentinal == False:
			return
		value = self.update(current_temp)
		self.write_PID(value)

			
	def terminate_heating(self):
		self.deactivate_relay()
		self.write_PID(0)
		
	#CHANGES THE RESISTANCE PROVIDED BY THE REHOSTAT TO THE DIMMER CONTROL ON THE HEATING ELEMENT POWER SUPPLY

	def write_PID(self, val):
		aval = self.bus.read_byte_data(ADDRESS, REG_A)
		bval = self.bus.read_byte_data(ADDRESS, REG_B)
		if val > 510:
			val = 510
		if val < 0:
			val = 0
		val = int(val)
		if val <= 255:
			if bval !=0:
				self.bus.write_byte_data(ADDRESS, REG_B, 0)
				return
			else:
				self.bus.write_byte_data(ADDRESS, REG_A, val)
		if val > 255:
			if aval != 255:
				self.bus.write_byte_data(ADDRESS, REG_A, 255)
				return
			else:
				bvalue = int(510 - val)
				self.bus.write_byte_data(ADDRESS, REG_B, bvalue)
		self.register_value.emit(val)
		print(val)
		aval = self.bus.read_byte_data(ADDRESS, REG_A)
		bval = self.bus.read_byte_data(ADDRESS, REG_B)
		print('setpoint val: ', val, 'REGISTER A set to: ', aval, 'REGISTER B set to:', bval)
		
		
	def update(self, current):
		self.__error = self.__setpoint - current
		
		self.__pvalue = self.__error * self.__kp
		
		self.__dvalue = self.__kd*(self.__error - self.__derivator)
		self.__derivator = self.__error
		
		self.__integrator = self.__integrator + self.__error
		if self.__integrator > 50:
			self.__integrator = 50
		elif self.__integrator < -50:
			self.__integrator = -50
			
		self.__ivalue = self.__ki*self.__integrator
		
		PID = self.__pvalue + self.__ivalue + self.__dvalue
		
		return PID
		

