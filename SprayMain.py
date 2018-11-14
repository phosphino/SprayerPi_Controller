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
from PyQt5.QtCore import pyqtSlot, QObject
from spray_control import spraycontrol
from pyqtTemp import *
import time 
import pyqtgraph as pg

pg.setConfigOption('foreground', 'y')
#pg.setConfigOption('background', 'b')
class mainwindow(Ui_MainWindow, QObject):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		QObject.__init__(self)
		self.setupUi(mainwindow)
		
		self.__spraysettingsDict = OrderedDict()
		self.__motorsettingsItems = []
		self.__motorlock = False
		self.__plotlock = False
		self.__syringe_params = {}
		self.__spray_params = {}
		self.__heating_sentinal = False
				
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
		self.newSetpoint_button.clicked.connect(self.go_to_setpoint)
		
		self.hotplate.register_value.connect(self.updateHeating_power)
		
		self.thermocouple.temperature_data.connect(self.updateTemperature)
		self.thermocouple.temperature_data.connect(self.hotplate.calculatePID)
		self.spraycontrol.operation_done.connect(self.unlockPlot)
		self.spraycontrol.sweep_complete.connect(self.updatePlot)
		
		self.dialog.calibrate_button.clicked.connect(self.calibrateTrack)
		self.dialog.testdelay_button.clicked.connect(self.test_motorSettings)
		self.startRun_button.clicked.connect(self.run_spraySynthesis)
		self.midpoint_button.clicked.connect(self.go_to_midpoint)

		
		self.temperature_QThread.started.connect(self.thermocouple.new_temp_emit)
		self.spray_QThread.started.connect(self.spraycontrol.perform_operation)
		

		self.hotplate.terminate_heating()
		
		self.temperature_QThread.start()
		
	def print_Check(self):
		print("THREAD FINISHED")
		
	def go_to_midpoint(self):
		if self.spray_QThread.isRunning():
			self.spray_QThread.exit()
		self.__plotlock = True
		self.spraycontrol.set_operationMode(3)
		self.spray_QThread.start()
	
	def go_to_setpoint(self):
		if self.__heating_sentinal == False:
			self.user_settings_error('Hotplate Disabled')
		else:
			setpoint = self.setPoint_edit.text()
			try:
				setpoint = float(setpoint)
			except:
				self.user_settings_error('Enter numeric temperature setpoint')
				return
			if setpoint < 0:
				self.user_settings_error('Setpoint must be a positive number')
				return
			
			self.hotplate.setPoint_start(setpoint)			
		
	def calibrateTrack(self):
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
		self.spraycontrol.set_track_width_inches(track_length)
		self.spraycontrol.set_operationMode(0)
		self.spray_QThread.start()
	
	def test_motorSettings(self):
		if self.spray_QThread.isRunning():
			self.spray_QThread.exit()
		try: 
			motor_delay = float(self.__spraysettingsDict[self.dialog.delay_label].text()) * 10**(-6)#convert microseconds to seconds
			microstepping = int(self.__spraysettingsDict[self.dialog.microstepping_label].currentIndex())
		except:
			self.user_settings_error('Input Valid Values')
		self.__plotlock = True
		self.spraycontrol.set_traverseParameters(motor_delay, microstepping)
		self.spraycontrol.set_operationMode(2)
		self.spray_QThread.start()
	
	def run_spraySynthesis(self):
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
		microstepping = int(self.__spraysettingsDict[self.dialog.microstepping_label].currentIndex())
		track_length = float(self.__spraysettingsDict[self.dialog.maxWidth_label].text())		
		spraymode = self.__spraysettingsDict[self.sprayMode_label].currentIndex()
		volume = float(self.__spraysettingsDict[self.dispenseVolume_label].text())
		vol_units = self.__spraysettingsDict[self.dispenseUnits_label].currentIndex()
		dispense_rate = float(self.__spraysettingsDict[self.dispenseRate_label].text())
		dispense_units = self.__spraysettingsDict[self.dispenseUnits_label].currentIndex()
		pause_time = float(self.__spraysettingsDict[self.pause_label].text())
		spray_width = float(self.__spraysettingsDict[self.sprayWidth_label].text())

		self.__spray_params = {'delay': motor_delay, 'pause_time' : pause_time, 'microstepping' : microstepping, 'width' : spray_width, 'mode' : spraymode}
		
		for key, value in self.__spray_params.items():
			print(key+':', value)
		
		self.spraycontrol.set_sprayParameters(self.__spray_params)
		
		try:
			self.__syringe_params = {'volume' : volume, 'vol_units' : vol_units, 'rate' : dispense_rate, 'rate_units' : dispense_units}
			
			for key, value in self.__syringe_params.items():
				print(key+':', value)
			
			self.spraycontrol.set_syringeSettings(**self.__syringe_params)
		except Exception as e:
			self.user_settings_error(str(e))
			return False
		return True

		
	def unlockPlot(self, boolean):
		if boolean:
			self.__plotlock = False
			if self.spray_QThread.isRunning():#exit thread upon completion of threaded operation
				self.spray_QThread.exit()

		
		
	def setup_settings_container(self):
		#add motor settings to settings dictionary
		self.__spraysettingsDict[self.dialog.delay_label] = self.dialog.delay_edit
		self.__spraysettingsDict[self.dialog.microstepping_label] = self.dialog.microstepping_comboBox
		self.__spraysettingsDict[self.dialog.maxWidth_label] = self.dialog.maxWidth_edit
		self.__spraysettingsDict[self.sprayMode_label] = self.sprayMode_comboBox
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
			self.hotplate.terminate_heating()
			self.hotplate_toggle.setText("Activate Hotplate")
			self.__heating_sentinal = False
			return
		else:	
			self.hotplate_toggle.setText("Disable Hotplate")
			self.__heating_sentinal = True
			
	@pyqtSlot(int)
	def updateHeating_power(self, register_value):
		print(register_value)
		percentage = 100.0*(float(register_value) / 510.0)
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
	
