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
from pyqtMpl import *
from stepper_control import motorcontrol
from pyqtTemp import *

class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		
		self.__spraymodes = ["Pneumatic","Ultrasonic"]
		
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

		self.mpl_widget = QtWidgets.QWidget()
		self.mpl = MplCanvas(self.mpl_widget)
		self.mpl_widget.setMinimumHeight(380)

		self.mpl_layout.addWidget(self.mpl)
		self.mpl_layout.addLayout(hbox)
		self.mpl_box.setLayout(self.mpl_layout)

		self.temp_lcd.resize(3, self.temp_lcd.height())

		# Bottom Half: spray options
		self.__sprayoptions = []
		self.__userinput = OrderedDict()

		self.spray_options_box = QtWidgets.QGroupBox("Spray Options")
		self.spray_options_layout = QtWidgets.QGridLayout(self.spray_options_box)		
		'''
		BEGIN: USER SETTINGS FOR SPRAY 
		'''
		self.mode_label = QtWidgets.QLabel("Mode Selected: ")
		self.mode_selected_label = QtWidgets.QLabel('None Selected')
		self.__sprayoptions.append([self.mode_label, self.mode_selected_label])

		self.set_temp_label = QtWidgets.QLabel("Set Point (Celsius): ")
		self.set_temp_edit = QtWidgets.QLineEdit()
		self.__sprayoptions.append([self.set_temp_label, self.set_temp_edit])
		
		self.set_volume_dispensing_label = QtWidgets.QLabel("Volume to dispense (mL): ")
		self.set_volume_dispensing_edit = QtWidgets.QLineEdit()
		self.__sprayoptions.append([self.set_volume_dispensing_label, self.set_volume_dispensing_edit])
		
		self.set_pause_label = QtWidgets.QLabel("Pause time (sec): ")
		self.set_pause_edit = QtWidgets.QLineEdit()
		self.__sprayoptions.append([self.set_pause_label, self.set_pause_edit])
		
		self.set_spray_width_label = QtWidgets.QLabel("Spray Travel Distance (inches): ")
		self.set_spray_width_edit = QtWidgets.QLineEdit()
		self.__sprayoptions.append([self.set_spray_width_label, self.set_spray_width_edit])
		'''
		END: USER SETTINGS FOR SPRAY
		
		'''
		for entry in self.__sprayoptions:
			self.__userinput[entry[0].text()] = entry[1]
		
		
		self.loaded_profile_label = QtWidgets.QLabel("Loaded Profile: ")
		self.loaded_profile_edit = QtWidgets.QLabel()
		self.__sprayoptions.append([self.loaded_profile_label, self.loaded_profile_edit])
		
		self.standby_button = QtWidgets.QPushButton("&Standby")
		self.__sprayoptions.append([self.standby_button])

		# for loop for putting elements in hbox and adding to vbox
		j = 0
		i = 0
		for z in range(len(self.__sprayoptions)):
			hbox = QtWidgets.QHBoxLayout()
			for x in self.__sprayoptions[z]:
				hbox.addWidget(x)
			self.spray_options_layout.addLayout(hbox, j, i)
			i = i+1
			if i > 2:
				i = 0
				j = j + 1

		self.spray_options_box.setLayout(self.spray_options_layout)
		self.main_grid = QtWidgets.QGridLayout(self.centralwidget)
		self.main_grid.addWidget(self.mpl_box, 0, 0)
		self.main_grid.addWidget(self.spray_options_box, 1, 0)
		'''
		END: POPULATE MAINWINDOW
		'''
		
		"""
		MenuBar Actions
		"""
		self.actionSave_Profile.triggered.connect(self.save_user_settings)
		self.actionLoad_Profile.triggered.connect(self.load_user_settings)
		
		self.actionPneumatic.triggered.connect(self.set_pneumatic)
		self.actionUltrasonic.triggered.connect(self.set_ultrasonic)
		
		self.actionSettings.triggered.connect(self.launch_settings)
		
		'''
		End MenuBar Actions
		'''
	
		self.__motor_connect = False
		self.m = motorcontrol()		
		self.standby_button.clicked.connect(self.run_test)

		x = np.linspace(0,10,1000)
		y = np.sin(x)
		self.mpl.update_figure(x,y)
		
	'''
	BEGIN: MENUBAR FUNCTIONS
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
		
		
	def set_pneumatic(self):
		self.__spraymode_selected = self.__spraymodes[0]
		self.__sprayoptions[0][1].setText(self.__spraymode_selected)
		
	def set_ultrasonic(self):
		self.__spraymode_selected = self.__spraymodes[1]
		self.__sprayoptions[0][1].setText(self.__spraymode_selected)
		
	def launch_settings(self):
		settings_dialog = QtWidgets.QDialog()
		dialog = Ui_MotorSettings()
		dialog.setupUi(settings_dialog)
		settings_dialog.exec_()
		settings_dialog.show()
		
		
	'''
	END: MENUBAR FUNCTIONS
	'''
	
	'''
	BEGIN: USER SETTINGS FUNCTIONS
	'''
	def get_user_spray_settings(self):
		output = []
		for key, value in self.__userinput.items():
			row = [key, value.text()]
			output.append(row)
		return output
		
	def set_user_spray_settings(self, settings):
		for row in settings:
			if row[0] in list(self.__userinput.keys()):
				self.__userinput[row[0]].setText(row[1])
			
			
	
	def check_settings(self):
		if self.__sprayoptions[0][1].text() not in self.__spraymodes:
			self.user_settings_error("Set Spray Mode")
			return False
		for entry in self.__sprayoptions[2:-2]:
			try:
				float(entry[1].text())
			except ValueError:
				self.user_settings_error("Enter Numeric Values For All Entries")
				return False
		return True
		
	def user_settings_error(self, message):
		error_dialog = QtWidgets.QMessageBox()
		error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
		error_dialog.setWindowTitle("!")
		error_dialog.setText(message)
		error_dialog.exec_()		
	
	'''
	END: USER SETTINGS FUNCTIONS
	'''
		
	def run_test(self):
		try:
			self.__spray_width = float(self.UI.set_spray_width_edit.text())
			self.__spray_speed = float(self.UI.set_sprayspeed_edit.text())
			self.__cycles = float(self.UI.set_spray_edit.text())
			self.__pause_time = float(self.UI.set_pause_edit.text())
			self.__spray_volume = float(self.UI.set_spray_volume_edit.text())
			m.go_to_midpoint()
			m.spray_cycle_motor(cycles = 10)
			print("hello")
		except:
			pass
		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)
	

	window.showMaximized()
	sys.exit(app.exec_())
	
