'''
Andrew Breuhaus-Alvarez, 2018
Model and Control code for Spray Pyrolysis Control Software
'''
import sys
from sprayUI import Ui_MainWindow
from settingsUI import Ui_MotorSettings
from PyQt5 import QtCore, QtWidgets, QtGui, QtSvg
from collections import OrderedDict
import csv
import numpy as np
from hotplate_control import thermocouplecontrol, hotplatecontrol
from spray_control import spraycontrol
from pyqtTemp import *
import time 
import pyqtgraph as pg

pg.setConfigOption('foreground', 'y')
#pg.setConfigOption('background', 'b')
class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		
		self.__spraysettingsDict = OrderedDict()
		self.__motorsettingsItems = []
		self.__motorlock = False
		self.__plotlock = False
				
		self.settings_dialog = QtWidgets.QDialog()
		self.dialog = Ui_MotorSettings()
		self.dialog.setupUi(self.settings_dialog)
		
		self.setup_settings_container()
		
		self.__plt = self.graphicsView
		self.__plt.setLabel('left','Temperature', 'Celsius')
		self.__plt.setLabel('bottom', 'Time', 'sec')
		
		self.dialog.microstepping_comboBox.setCurrentIndex(2)
		
		self.hotplate = hotplatecontrol()
		self.thermocouple = thermocouplecontrol()
		self.spraycontrol = spraycontrol()
		
		self.__thermocouple_time = [0]
		self.__thermocouple_temp = [self.thermocouple.thermocouple.temp()]
		self.__curve = self.__plt.plot(pen = 'm')
		
		
		self.spray_QThread = QtCore.QThread()#Thread for performing calibrations
		self.temperature_QThread = QtCore.QThread()#Thread for monitoring temperature
		
		self.thermocouple.moveToThread(self.temperature_QThread)
		self.spraycontrol.moveToThread(self.spray_QThread)
		
		
		
		'''
		BEGIN: SIGNAL/SLOT 
		
		'''
		self.actionSettings.triggered.connect(self.launch_settings)
		self.actionSave_Profile.triggered.connect(self.save_settings)
		self.actionLoad_Profile.triggered.connect(self.load_settings)
		
		self.clearPlot_button.clicked.connect(self.clear_plot)
		self.hotplate_toggle.clicked.connect(self.toggle_heating)
		
		self.thermocouple.temperature_data.connect(self.updateTemperature)
		self.thermocouple.temperature_data.connect(self.hotplate.calculatePID)
		self.spraycontrol.operation_done.connect(self.unlockPlot)
		
		self.dialog.calibrate_button.clicked.connect(self.setMode_Calibrate)
		self.startRun_button.clicked.connect(self.setMode_Run)
		
		self.spraycontrol.motor_sweep_complete.connect(self.updatePlot)
		self.temperature_QThread.started.connect(self.thermocouple.new_temp_emit)
		self.spray_QThread.started.connect(self.spraycontrol.perform_operation)
		
		
		
		self.hotplate.register_value.connect(self.updateHeating_power)
		self.hotplate.terminate_heating()
		
		self.temperature_QThread.start()
		
	def print_Check(self):
		print("THREAD FINISHED")
		
	def setMode_Calibrate(self):
		if self.spray_QThread.isRunning():
			self.spray_QThread.exit()
		try:
			track_length = float(self.__spraysettingsDict[self.dialog.maxWidth_label].text())
			if track_length < 0:
				self.user_settings_error('Track length must be greater than zero')
				return
		except:
			self.user_settings_error('Input a numeric value for track length')
			return
		
		self.__plotlock = True
		self.spraycontrol.stepperMotor.set_track_width_inches(track_length)
		self.spraycontrol.set_operationMode(0)
		self.spray_QThread.start()
	
	def setMode_Run(self):
		if self.spray_QThread.isRunning():
			self.spray_QThread.exit()
		
		if self.setMotorSpray_settings():
			self.__plotlock = True
			self.spraycontrol.set_operationMode(1)
			self.spray_QThread.start()
	
	def setMotorSpray_settings(self):
		if self.check_settings == False:
			return False
		motor_delay = float(self.__spraysettingsDict[self.dialog.delay_label].text()) * 10**(-6)#convert microseconds to seconds
		print('motor delay ', motor_delay)
		microstepping = int(self.__spraysettingsDict[self.dialog.microstepping_label].currentIndex())
		print('microstepping key: ',microstepping)
		track_length = float(self.__spraysettingsDict[self.dialog.maxWidth_label].text())
		print('track length: ', track_length)
		self.spraycontrol.setMotor_settings(motor_delay, microstepping, track_length)
		
		spraymode = self.__spraysettingsDict[self.sprayMode_label].currentIndex()
		print('spraymode: ',spraymode)
		cycles = int(self.__spraysettingsDict[self.sprayNumber_label].text())
		print('cycles: ', cycles)
		volume = float(self.__spraysettingsDict[self.dispenseVolume_label].text())
		print('volume: ', volume)
		vol_units = self.__spraysettingsDict[self.dispenseUnits_label].currentIndex()
		print('vol_units key: ', vol_units)
		dispense_rate = float(self.__spraysettingsDict[self.dispenseRate_label].text())
		print('dispense_rate: ', dispense_rate)
		dispense_units = self.__spraysettingsDict[self.dispenseUnits_label].currentIndex()
		print('dispense_units key: ', dispense_units)
		pause_time = float(self.__spraysettingsDict[self.pause_label].text())
		print('pause time: ', pause_time)
		spray_width = float(self.__spraysettingsDict[self.sprayWidth_label].text())
		print('spray_width: ', spray_width)
		try:
			self.spraycontrol.setSpray_settings(spraymode, cycles, volume, vol_units, dispense_rate, dispense_units, pause_time, spray_width)
		except Exception as e:
			self.user_settings_error(str(e))
			return False
		return True
	'''	
	def setMotor_settings(self, motor_delay, microstepping, track_length):
		self.stepperMotor.set_delay(motor_delay)
		self.stepperMotor.set_microstepping(microstepping)
		self.stepperMotor.set_track_width(track_length)
		
	def setSpray_settings(self, spraymode, cycles, volume, vol_units, dispense_rate,
							dispense_units, pause_time, spray_width):
				
		self.__selectedSpray_mode = spraymode
		self.syringePump.setRate(dispense_rate, units = dispense_units)
		self.syringePump.set_dispense_volume(volume, units = vol_units)
		self.stepperMotor.setPause_time(pause_time)
		self.stepperMotor.setSpray_width(spray_width)
		self.stepperMotor.setCycle_number(cycles)
	'''
		
	def unlockPlot(self, boolean):
		if boolean:
			self.__plotlock = False

		
		
	def setup_settings_container(self):
		#add motor settings to settings dictionary
		self.__spraysettingsDict[self.dialog.delay_label] = self.dialog.delay_edit
		self.__spraysettingsDict[self.dialog.microstepping_label] = self.dialog.microstepping_comboBox
		self.__spraysettingsDict[self.dialog.maxWidth_label] = self.dialog.maxWidth_edit
		self.__spraysettingsDict[self.sprayMode_label] = self.sprayMode_comboBox
		self.__spraysettingsDict[self.sprayNumber_label] = self.sprayNumber_edit
		self.__spraysettingsDict[self.dispenseVolume_label] = self.dispenseVolume_edit
		self.__spraysettingsDict[self.dispenseUnits_label] = self.dispenseUnits_comboBox
		self.__spraysettingsDict[self.dispenseRate_label] = self.dispenseRate_edit
		self.__spraysettingsDict[self.rateUnits_label] = self.rateUnits_comboBox
		self.__spraysettingsDict[self.pause_label] = self.pause_edit
		self.__spraysettingsDict[self.sprayWidth_label] = self.sprayWidth_edit
		self.__spraysettingsDict[self.setPoint_label] = self.setPoint_edit
		
		
	def check_settings(self):
		try:
			temporary_delay = float(self.__spraysettingsDict[self.dialog.delay_label].text())
			if temporary_delay < 1 or temporary_delay > 2000:
				self.user_settings_error('File->Settings: motor delay out of range')
				return False
		except:
			self.user_settings_error('File->Settings: motor delay must be numeric')
			return False
		
		try:
			temporary_maxWidth = float(self.__spraysettingsDict[self.dialog.maxWidth_label].text())
			if temporary_maxWidth <= 0:
				self.user_settings_error('File->Settings: track width must be a positive, non-zero value')
				return False
		except:
			self.user_settings_error('File->Settings: track width must be numeric')
			return False
			
		try:
			temporary_cycleNumber = int(self.__spraysettingsDict[self.sprayNumber_label].text())
			if temporary_cycleNumber <=0:
				self.user_settings_error('Number of spray cycles must be a positive number')
			
		except:
			self.user_settings_error('Number of spray cycles must be numeric')
			return False
				
		
		try:
			temporary_volume = float(self.__spraysettingsDict[self.dispenseVolume_label].text())
			if temporary_volume <= 0:
				self.user_settings_error('Dispense volume must be a positive, non-zero value')
				return False
		except:
			self.user_settings_error('Dispense Volume must be numeric')
			return False
			
		try:
			temporary_rate = float(self.__spraysettingsDict[self.dispenseRate_label].text())
			if temporary_rate <=0:
				self.user_settings_error('Dispensing rate must be a positive, non-zero value')
				return False
		
		except:
			self.user_settings_error('Dispensing rate must be numeric')
			return False
			
		try:
			temporary_pause = float(self.__spraysettingsDict[self.pause_label].text())
			if temporary_pause < 0:
				self.user_settings_error('Pause time must be a positive, non-zero value')
				return False
		
		except:
			self.user_settings_error('Pause time must be numeric')
			return False
		
		try:
			temporary_width = float(self.__spraysettingsDict[self.sprayWidth_label].text())
			if temporary_width <=0 or temporary_width > temporary_maxWidth:
				self.user_settings_error('Spray width must be greater than zero and less than the track width')
				return False
				
		except:
			self.user_settings_error('Spray width must be numeric')
			return False
		
		try:
			temporary_setpoint = float(self.__spraysettingsDict[self.setPoint_label].text())
			if temporary_setpoint < 0 or temporary_setpoint > 750:
				self.user_settings_error('Hotplate setpoint out of range')
				return False
		
		except:
			self.user_settings_error('Hotplate setpoint must be numeric')
			return False	
	
	def get_save_settings(self):
		settings = []
		for key, value in self.__spraysettingsDict.items():
			#Check if value is a comboBox
			if type(value) == type(self.dialog.microstepping_comboBox):
				entry = [key.text(), value.currentText()]
				settings.append(entry)
			else:
				entry = [key.text(), value.text()]
				settings.append(entry)
		return settings
	
	def save_settings(self):
		if self.check_settings() == False:
			return 
		file_name = QtWidgets.QFileDialog.getSaveFileName(None, 'Save Settings', '/home/Documents/GitHub/', "CSV (*.csv)")
		settings_name = file_name[0].split('/')[-1].split('.')[0]
		settings = self.get_save_settings()
		save_name = file_name[0]
		if ".csv" not in save_name:
			save_name = save_name+".csv"	
		output_file = open(save_name, 'w', newline='')
		output_writer = csv.writer(output_file)
		for row in settings:
			output_writer.writerow(row)
		output_file.close()	
		self.loadedProfile_label.setText(settings_name)
		
	def load_settings(self):
		file_name = QtWidgets.QFileDialog.getOpenFileName(None, 'Open Material Settings', '/home/Documents/GitHub/', "CSV (*.csv)") 
		settings_name = file_name[0].split('/')[-1].split('.')[0]
		open_file = file_name[0]
		try:
			input_file = open(open_file)
		except:
			self.user_settings_error('INVALID FILE')
			return
		input_settings = list(csv.reader(input_file))
		input_file.close()
		
		#setting the settings
		for row in input_settings:
			for key, value in self.__spraysettingsDict.items():
				if row[0] == key.text():
					if type(value) == type(self.dialog.microstepping_comboBox):
						index = value.findText(row[1])
						if index == -1:
							self.user_settings_error('INVALID FILE')
							return
						value.setCurrentIndex(index)
					else:
						value.setText(row[1])
		self.loadedProfile_label.setText(settings_name)
		
	def updateTemperature(self, val):
		self.__thermocouple_time.append(self.__thermocouple_time[-1]+ 1)
		self.__thermocouple_temp.append(val)

		if self.__plotlock == False:
			self.updatePlot()		
		self.currentTemp_lcd.display(val)
		
	def updatePlot(self):
		#disableAutoRange then plot then enableAutoRange instead of just keeping enableAutoRange() always enabled increases speed of plotting according to internet
		#self.__plt.disableAutoRange
		self.__curve.setData(self.__thermocouple_time, self.__thermocouple_temp)
		#self.__plt.enableAutoRange()
				
	def toggle_heating(self):
		print(self.hotplate.query_relay())
		if self.hotplate.query_relay()==1:
			print('turning off')
			self.hotplate.terminate_heating()
			self.hotplate_toggle.setText("Hotplate ON")
			return
			
		try:
			setpoint = float(self.__spraysettingsDict[self.setPoint_label].text())
		except:
			self.user_settings_error('Temperature Setpoint Invalid')
			return
		print('turning on')
		self.hotplate.setPoint_start(setpoint)
		self.hotplate_toggle.setText("Hotplate OFF")
		
	def updateHeating_power(self, register_value):
		percentage = 100.0*(float(register_value) / 255.0)
		self.hotplatePercent_label.setText('{0:.1f} %'.format(percentage))
		
		
	def launch_settings(self):
		self.settings_dialog.show()
		self.settings_dialog.exec_()

	def clear_plot(self):
		self.__plt.clear()
		self.__thermocouple_time = [0]
		self.__thermocouple_temp = [self.thermocouple.thermocouple.temp()]
		self.__curve = self.__plt.plot(pen='c')
		
	def user_settings_error(self, message):
		error_dialog = QtWidgets.QMessageBox()
		error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
		error_dialog.setWindowTitle("!")
		error_dialog.setText(message)
		error_dialog.exec_()		
	


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)
	

	window.showMaximized()
	sys.exit(app.exec_())
	
