'''
Andrew Breuhaus-Alvarez, September 2018
Bartlett Lab
python3
class for controlling New-Era NE-1000 syringe pump. 
baudrate must match baudrate set on syringe pump. default 19200
Design influenced by Will Dickinson's control class
https://bitbucket.org/iorodeo/syringe_pump/overview
'''

import time
import serial
import sys

port='/dev/ttyUSB0'
baudrate = 19200
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE
bytesize=serial.EIGHTBITS
timeout = 0.1

class syringecontrol(serial.Serial):
	def __init__(self, syringe_diameter = 14.5673):
		para = {
				'port' : port,
				'baudrate' : baudrate,
				'parity' : parity,
				'stopbits' : stopbits,
				'timeout' : timeout,
				}
		super(syringecontrol,self).__init__(**para)
		time.sleep(0.35)#NEED THIS SLEEP COMMAND TO ALLOW FOR CONNECTION HANDSHAKE/SETUP OR WHATEVER
		#WITHOUT THIS SLEEP, COMMANDS IN __INIT__ ARE HAVING NO EFFECT
		
		self.__addr = str(00) #Address of syringe pump
		#address is optional if pump address is 00 but used here for clarity
		
		self.__rateunits = {
							2 : 'UM*',
							0 : 'MM*',
							3 : 'UH*',
							1 : 'MH*'
								}
		
		self.__rsp = None
		'''
		CANNOT DIRECTLY RETURN SYRINGE PUMP RESPONSE FROM self.readline(). 
		HOWEVER IF I print(self.readline()), THEN THE EXPECTED RESPONSE IS PRINTED.
		IF I return self.readline(), IT RETURNS NONE FOR ALL COMMANDS.
		IF I DUMP self.readline() INTO self.__rsp AND THEN DECODE AND READ, IT WORKS.
		NOT SURE WHY THIS HAPPENS SO USING THIS WORK AROUND.
		PROBABLY DOING SOMETHING WRONG. whatever
		'''
	
		self.clear_volume_dispensed()
		self.set_diameter(syringe_diameter)
		self.write_command('VOLML') #set syringe volume units to mL.
		#unit conversion occurs software side
		self.loc_keypad(False)
		self.__run_state = False
		
	def write_command(self, command):
		command = self.__addr+command+'\x0D'#PREPEND PUMP ADDRESS AND APPEND CARRIAGE RETURN 
		self.write(command.encode('utf8'))#ENCODE COMMAND AS ASCII
		receive = self.readline()
		self.__rsp = receive#SET THE DUMMY VARIABLE self.__rsp to the response
		#self.__rsp must be used immediately after calling write_command() to prevent
		#corruption of data
		self.decode_response()
		return self.__rsp
	
	def decode_response(self):#WORK AROUND FOR RETURNING SYRINGE PUMP RESPONSE
		self.__rsp = self.__rsp[1:-1].decode()		
				
	def loc_keypad(self, boolean):
		if boolean:
			command = 'LOC1' #LOCK KEYPAD ON SYRINGE PUMP	
		else:
			command = 'LOC0' #DISABLE KEYPAD LOCK
			
		response = self.write_command(command)
		if '?' in response:
			raise Exception('loc_keypad')
		return response
	
	def set_diameter(self, dia):#SYRINGE DIAMETER IN MILLIMETERS
		command = 'DIA'+self.formatfloat(dia)
		response = self.write_command(command)
		if '?' in response:
			raise Exception('set_diameter')
		return response
		
	def get_diameter(self):#RETURN SYRINGE DIAMETER IN MILLIMETERS
		command = 'DIA'
		response = self.write_command(command)
		if '?' in response:
			raise Exception('get_diameter')
		response = response[3:]
		response = float(response)
		return response
		
	#SET DISPENSING RATE
	def set_rate(self, rate, units = 0):
		command = 'RAT'+self.formatfloat(rate)+self.__rateunits[units]
		response = self.write_command(command)
		if '?' in response:
			raise Exception('Rate OOR for given units')
		return response
	
	def get_rate(self):
		command = 'RAT'
		response = self.write_command(command)
		return response
		
	#SET VOLUME TO BE DISPENSED
	def set_dispense_volume(self, vol, units=0):
		if units == 0:
			command = 'VOLML'
			response = self.write_command(command)
			if '?' in response:
				raise Exception('error in VOL mL unit change')
		elif units == 1:
			command = 'VOLUL'
			response = self.write_command(command)
			if '?' in response:
				raise Exception('error in VOL uL unit change')
		else:
			raise Exception('INCORRECT UNITS')
		command = 'VOL'+self.formatfloat(vol)
		response = self.write_command(command)
		if '?' in response:
			raise Exception('set_dispense_volume')
		return response
	
	#RETURN THE VOLUME THAT IS SET TO BE DISPENSED
	#RETURNS TUPLE
	def get_dispense_volume(self):
		command = 'VOL'
		response = self.write_command(command)
		if '?' in response:
			raise Exception('get_dispense_volume')
		response = response[3:]
		print(response)
		response = (float(response[:-2]),response[-2:])
		return response

	#RETURNS THE VOLUME THAT HAS ALREADY BEEN DISPENSED
	#RETURNS TUPLE
	def get_volume_dispensed(self):
		command = 'DIS'
		response = self.write_command(command)
		if '?' in response:
			raise Exception('get_volume_dispensed')
		response = (float(response[4:9]), response[-2:])
		return response
		
	def clear_volume_dispensed(self):
		command = 'CLDINF'
		self.write_command(command)
		command = 'CLDWDR'
		self.write_command(command)
	
	def set_pump_dir(self, DIR):
		directions = {'infuse' : 'INF', 'withdraw' : 'WDR', 'reverse' : 'REV'}
		command = 'DIR'+directions[DIR]
		response = self.write_command(command)
		if '?' in response:
			raise Exception('set_pump_dir')
		return response
		
	def get_pump_dir(self):
		command = 'DIR'
		response = self.write_command(command)
		if '?' in response:
			raise Exception('get_pump_dir')
		response = response[-3:]
		return response
		
	def run_pump(self):
		command = 'RUN'
		response = self.write_command(command)
		return response
	
	def stop_pump(self):
		command = 'STP'
		response = self.write_command(command)
		return response
		
	def purge_pump(self):
		command = 'PUR'
		response = self.write_command(command)
		return response
	
	def return_rsp(self):
		return self.__rsp

	def formatfloat(self, fl):
		fl = float(fl)
		if fl < 0 or fl >= 1000:
			raise ValueError('OUT OF RANGE')
		if fl >= 100:
			str_float = '{0:3.1f}'.format(fl)
		elif fl >= 10:
			str_float = '{0:2.2f}'.format(fl)
		else:
			str_float = '{0:1.3f}'.format(fl)
		return str_float
		

