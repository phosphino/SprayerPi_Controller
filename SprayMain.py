import sys
from sprayUI import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
from pyqtMpl import *
from pyqtTemp import *
import RPi.GPIO as GPIO

class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		
		#GPIO setup
		GPIO.setmode(GPIO.BOARD)#Using Physical Pin Numbers		
		GPIO.setwarnings(False)
		
		#Timer setup
		self.timer = QtCore.QTimer()
		self.interval = 1500
		
		#Thermocouple setup
		self.thermocouple = adatemp()
		self.time = [0]
		self.temp = [self.thermocouple.temp()]
				
		#GPIO setup: Hotplate
		self.gpio_hotplate = 8 #hotplate relay is connected to pin #8 
		GPIO.setup(self.gpio_hotplate, GPIO.OUT, initial=GPIO.LOW)

		#Quadrant 1: matplotlib widget and object
		self.mpl_widget = QtWidgets.QWidget()
		self.mpl = MplCanvas(self.mpl_widget)
		self.mpl_widget.setMinimumHeight(380)

		#Quadrant 2: spray options
		sprayoptions = []
		self.spray_options_box = QtWidgets.QGroupBox("Spray Options")
		self.spray_options_layout = QtWidgets.QVBoxLayout()
		
		self.set_temp_label = QtWidgets.QLabel("Set Point (Celsius): ")
		self.set_temp_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_temp_label, self.set_temp_edit])
		
		self.set_spray_label = QtWidgets.QLabel("Number of sprays: ")
		self.set_spray_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spray_label, self.set_spray_edit])
		
		self.set_sprayspeed_label = QtWidgets.QLabel("Set Move Speed")
		self.set_sprayspeed_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_sprayspeed_label, self.set_sprayspeed_edit])
		
		self.set_spraypause_label = QtWidgets.QLabel("Set pause time (sec)")
		self.set_spraypause_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spraypause_label, self.set_spraypause_edit])
		
		self.heating_status = QtWidgets.QLabel("Heating Off")
		sprayoptions.append([self.heating_status])
		
		self.spraying_status = QtWidgets.QLabel("Spraying Off")
		sprayoptions.append([self.spraying_status])
		
		self.loaded_profile_label = QtWidgets.QLabel("Loaded Profile: ")
		self.loaded_profile_edit = QtWidgets.QLabel()
		sprayoptions.append([self.loaded_profile_label, self.loaded_profile_edit])
		
		#for loop for putting elements in hbox and adding to vbox
		for x in sprayoptions:
			hbox = QtWidgets.QHBoxLayout()
			for i in x:
				hbox.addWidget(i)
			self.spray_options_layout.addLayout(hbox)	
		
		self.spray_options_box.setLayout(self.spray_options_layout)
		self.spray_options_box.resize(300,300)
		self.spray_options_box.setMaximumWidth(300)
		
		self.spray_options_box.setMaximumHeight(250)

		#Quadrant 3: spray_control
		self.spray_control_box = QtWidgets.QGroupBox("Spray Control")
		self.spray_control_layout = QtWidgets.QVBoxLayout()

		#Quadrant 4: spray_progress
		self.spray_progress_layout = QtWidgets.QVBoxLayout()


		#Setup Layout
		self.main_grid = QtWidgets.QGridLayout(self.centralwidget)
		self.main_grid.addWidget(self.mpl_widget, 0, 1)
		self.main_grid.addWidget(self.spray_options_box, 0, 0)
		
		#Connect QTimer for Updating
		self.timer.timeout.connect(self.update_temperature)
		self.timer.start(self.interval)
		
		
		
	def heat_on(self):
		GPIO.output(self.gpio_hotplate, GPIO.HIGH)
	
	def heat_off(self):
		GPIO.output(self.gpio_hotplate, GPIO.LOW)
	
		
	def update_temperature(self):
		temp = self.thermocouple.temp()
		self.time.append(self.time[-1]+(self.interval/1000.0))
		self.temp.append(temp)
		self.mpl.update_figure(self.time,self.temp)
		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)

	window.show()
	sys.exit(app.exec_())
