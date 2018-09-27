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


class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		
		self.__settingsDict = OrderedDict()
		self.__settingsDictKeys = None
				
		self.settings_dialog = QtWidgets.QDialog()
		self.dialog = Ui_MotorSettings()
		self.dialog.setupUi(self.settings_dialog)
		
		self.setup_settings_container()
		
		self.__plt = self.graphicsView
		self.__plt.setLabel('left','Temperature', 'Celsius')
		self.__plt.setLabel('bottom', 'Time', 'seconds')
		self.__plt.enableAutoRange()
		
		self.dialog.microstepping_comboBox.setCurrentIndex(2)
		
		self.setup_settings_container()
		
		self.thermocouple = thermocouplecontrol(self.__plt)
		
		

		
		'''
		BEGIN: SETUP SETTINGS DIALOG WINDOW
		'''

		
		'''
		BEGIN: SIGNAL/SLOT 
		'''
		self.actionSettings.triggered.connect(self.launch_settings)
		self.actionSave_Profile.triggered.connect(self.save_settings)
		self.thermocouple.temperature_data.connect(self.updateLCD)
		#self.actionLoad_Profile.triggered.connect(self.load_settings)
		
		self.thermocouple.start()
		
	def setup_settings_container(self):
		self.__settingsDict[self.dialog.delay_label] = self.dialog.delay_edit
		self.__settingsDict[self.dialog.microstepping_Label] = self.dialog.microstepping_comboBox
		self.__settingsDict[self.dialog.maxWidth_label] = self.dialog.maxWidth_edit
		self.__settingsDict[self.sprayMode_label] = self.sprayMode_comboBox
		self.__settingsDict[self.dispenseVolume_label] = self.dispenseVolume_edit
		self.__settingsDict[self.dispenseUnits_label] = self.dispenseUnits_comboBox
		self.__settingsDict[self.dispenseRate_label] = self.dispenseRate_edit
		self.__settingsDict[self.rateUnits_label] = self.rateUnits_comboBox
		self.__settingsDict[self.pause_label] = self.pause_edit
		self.__settingsDict[self.sprayWidth_label] = self.sprayWidth_edit
		self.__settingsDict[self.setPoint_label] = self.setPoint_edit
		
		self.__settingsDictKeys = list(self.__settingsDict.keys())
		
	def check_settings(self):
		try:
			temporary_delay = float(self.__settingsDict[self.dialog.delay_label].text())
			if temporary_delay < 200 or temporary_delay > 500:
				self.user_settings_error('File->Settings: motor delay out of range')
				return False
		except:
			self.user_settings_error('File->Settings: motor delay must be numeric')
			return False
		
		try:
			temporary_maxWidth = float(self.__settingsDict[self.dialog.maxWidth_label].text())
			if temporary_maxWidth <= 0:
				self.user_settings_error('File->Settings: track width must be a positive, non-zero value')
				return False
		except:
			self.user_settings_error('File->Settings: track width must be numeric')
			return False
		
		try:
			temporary_volume = float(self.__settingsDict[self.dispenseVolume_label].text())
			if temporary_volume <= 0:
				self.user_settings_error('Dispense volume must be a positive, non-zero value')
				return False
		except:
			self.user_settings_error('Dispense Volume must be numeric')
			return False
			
		try:
			temporary_rate = float(self.__settingsDict[self.dispenseRate_label].text())
			if temporary_rate <=0:
				self.user_settings_error('Dispensing rate must be a positive, non-zero value')
				return False
		
		except:
			self.user_settings_error('Dispensing rate must be numeric')
			return False
			
		try:
			temporary_pause = float(self.__settingsDict[self.pause_label].text())
			if temporary_pause <= 0:
				self.user_settings_error('Pause time must be a positive, non-zero value')
				return False
		
		except:
			self.user_settings_error('Pause time must be numeric')
			return False
		
		try:
			temporary_width = float(self.__settingsDict[self.sprayWidth_label].text())
			if temporary_width <=0 or temporary_width > temporary_maxWidth:
				self.user_settings_error('Spray width must be greater than zero and less than the track width')
				return False
				
		except:
			self.user_settings_error('Spray width must be numeric')
			return False
		
		try:
			temporary_setpoint = float(self.__settingsDict[self.setPoint_label].text())
			if temporary_setpoint < 0 or temporary_setpoint > 750:
				self.user_settings_error('Hotplate setpoint out of range')
				return False
		
		except:
			self.user_settings_error('Hotplate setpoint must be numeric')
			return False	
		
				
			

	
	def save_settings(self):
		if self.check_settings() == False:
			return 
		pass
		
		
	def updateLCD(self, val):
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
	
