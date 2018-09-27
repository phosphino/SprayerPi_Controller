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
from pyqtMpl import *
from threading import Thread
import time 
import atexit

class mainwindow(QtWidgets.QMainWindow,Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		
		self.mpl_widget = QtWidgets.QWidget()
		self.mpl = MplCanvas(self.mpl_widget)
		self.mpl_widget.setMinimumHeight(380)
		
		self.thermocouple = thermocouplecontrol(self.mpl)
		
		self.horizontal_spacer = QtWidgets.QSpacerItem(500, 10, QtWidgets.QSizePolicy.Expanding)
		
		'''
		BEGIN: VARIABLES FOR HOTPLATE
		'''
		
		self.__previoustemp = self.thermocouple.thermocouple.temp()
		self.__previoustime = 0.0
		self.__temperature_data = [[self.__previoustime],[self.__previoustemp]]
		
		'''
		END: VARIABLES FOR HOTPLATE
		'''
		
		'''
		BEGIN: POPULATE MAIN WINDOW
		'''
		self.spray_settings = []
		# Top Half: matplotlib widget and object
		self.mpl_box = QtWidgets.QGroupBox("Temperature")
		self.mpl_layout = QtWidgets.QVBoxLayout()

		self.temp_lcd = QtWidgets.QLCDNumber()
		self.temp_lcd_label = QtWidgets.QLabel("Current Temperature (Celsius)")
		self.temp_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)

		hbox = QtWidgets.QHBoxLayout()
		hbox.addWidget(self.temp_lcd_label)
		hbox.addWidget(self.temp_lcd)
		hbox.addSpacerItem(self.horizontal_spacer)



		self.mpl_layout.addWidget(self.mpl)
		self.mpl_layout.addLayout(hbox)
		self.mpl_box.setLayout(self.mpl_layout)

		self.temp_lcd.resize(3, self.temp_lcd.height())
		self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.main_layout.addWidget(self.mpl_box)
		



		
		'''
		BEGIN: SETUP SETTINGS DIALOG WINDOW
		'''
		
		self.settings_dialog = QtWidgets.QDialog()
		self.dialog = Ui_MotorSettings()
		self.dialog.setupUi(self.settings_dialog)
		
		'''
		BEGIN: SIGNAL/SLOT 
		'''
		self.actionSettings.triggered.connect(self.launch_settings)
		
		#self.thermocouple.start()


	'''
	BEGIN FUNCTIONS UTILIZING HOTPLATE_CONTROL.PY
	'''


		
	def save_user_settings(self):
		if self.check_settings() == False:
			return
		fname = QtWidgets.QFileDialog.getSaveFileName(None, 'Save Material Settings', '/home/Documents/GitHub/', "CSV (*.csv)")	
		current_settings = self.get_user_spray_settings()
		save_file = fname[0]
		if ".csv" not in save_file:
			save_file = save_file+".csv"
		output_file = open(save_file, 'w', newline='')
		output_writer = csv.writer(output_file)
		for row in current_settings:
			output_writer.writerow(row)
		output_file.close() 
		
	def load_user_settings(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open Material Settings', '/home/Documents/GitHub/', "CSV (*.csv)")		
		settings_name = fname[0].split('/')[-1].split('.')[0]
		open_file = fname[0]
		try: 
			input_file = open(open_file)
			
		except: 
			self.user_settings_error("INVALID FILE")
			return
		input_settings = list(csv.reader(input_file))
		self.set_user_spray_settings(input_settings)
		self.loaded_profile_edit.setText(settings_name)	
		input_file.close()
		

		
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
	
