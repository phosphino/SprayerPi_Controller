'''
Andrew Breuhaus-Alvarez, 2018
Model and Control code for Spray Pyrolysis Control Software
'''
import sys
from sprayUI import Ui_MainWindow
from settingsUI import Ui_MotorSettings
from PyQt5 import QtCore, QtWidgets, QtGui
from collections import OrderedDict
import csv
import numpy as np
from hotplate_control import thermocouplecontrol
from pyqtTemp import *
import time 
import pyqtgraph as pg

pg.setConfigOption('foreground', 'y')

class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		
		self.__spraysettingsDict = OrderedDict()
		self.__motorsettingsItems = []
				
		self.settings_dialog = QtWidgets.QDialog()
		self.dialog = Ui_MotorSettings()
		self.dialog.setupUi(self.settings_dialog)
		
		self.setup_settings_container()
		
		self.__plt = self.graphicsView
		self.__plt.setLabel('left','Temperature', 'Celsius')
		self.__plt.setLabel('bottom', 'Time', 'seconds')
		
		self.dialog.microstepping_comboBox.setCurrentIndex(2)
		
		self.thermocouple = thermocouplecontrol()
		self.__thermocouple_time = [0]
		self.__thermocouple_temp = [self.thermocouple.thermocouple.temp()]
		
		self.__plt.plot(self.__thermocouple_time, self.__thermocouple_temp)
		self.__curve = self.__plt.plot(pen = 'c')
		

		
		'''
		BEGIN: SETUP SETTINGS DIALOG WINDOW
		'''

		
		'''
		BEGIN: SIGNAL/SLOT 
		'''
		self.actionSettings.triggered.connect(self.launch_settings)
		self.actionSave_Profile.triggered.connect(self.save_settings)
		self.thermocouple.temperature_data.connect(self.updateTemperature)
		#self.actionLoad_Profile.triggered.connect(self.load_settings)
		
		self.thermocouple.start()
		
	def setup_settings_container(self):
		#add motor settings to settings dictionary
		self.__spraysettingsDict[self.dialog.delay_label] = self.dialog.delay_edit
		self.__spraysettingsDict[self.dialog.microstepping_Label] = self.dialog.microstepping_comboBox
		self.__spraysettingsDict[self.dialog.maxWidth_label] = self.dialog.maxWidth_edit
		#need a list which keeps track of which settings go in the dialog
		for key, value in self.__spraysettingsDict.items():
			self.__motorsettingsItems.append(key.text())		
		print(self.__motorsettingsItems)
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
			if temporary_delay < 200 or temporary_delay > 500:
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
			if temporary_pause <= 0:
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
			if type(value) == type(self.dialog.microstepping_comboBox):
				entry = [key.text(), value.currentText()]
				settings.append(entry)
		print(settings)
	
	def save_settings(self):
		#if self.check_settings() == False:
			#return 
		#file_name = QtWidgets.QFileDialog.getSaveFileName(None, 'Save Settings', '/home/Documents/GitHub/', "CSV (*.csv)")
		settings = self.get_save_settings()
		
		
		
	def updateTemperature(self, val):
		self.__thermocouple_time.append(self.__thermocouple_time[-1]+ 1)
		self.__thermocouple_temp.append(val)
		#if len(self.__thermocouple_time) > 60:
		#	self.__thermocouple_time.pop(0)
		#	self.__thermocouple_temp.pop(0)
		#	print(self.__thermocouple_time[0])
		#self.__curve.disableAutoRange()
		#self.__plt.plot(self.__thermocouple_time, self.__thermocouple_temp)
		self.__curve.setData(self.__thermocouple_time, self.__thermocouple_temp)
		#self.__curve.enableAutoRange()
		self.currentTemp_lcd.display(val)
		
	def launch_settings(self):
		self.settings_dialog.show()
		self.settings_dialog.exec_()


		
	def user_settings_error(self, message):
		error_dialog = QtWidgets.QMessageBox()
		error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
		error_dialog.setWindowTitle("!")
		error_dialog.setText(message)
		error_dialog.exec_()		
	
	'''
	END: USER SETTINGS FUNCTIONS
	'''
	
		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)
	

	window.showMaximized()
	sys.exit(app.exec_())
	
