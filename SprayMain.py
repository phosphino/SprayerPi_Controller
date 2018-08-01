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
		

		self.target_temp_edit = QtWidgets.QLineEdit()
		self.target_temp_label = QtWidgets.QLabel("Target T (Celsius)")

		self.number_of_sprays = QtWidgets.QLineEdit()
		self.number_of_sprays_label = QtWidgets.QLabel("# of Sprays")

		self.heating_boolean = False
		self.heating_on_label = "Heater On"
		self.heating_off_label = "Heater Off"

		self.spray_boolean = False
		self.spray_on_label = "Spray On"
		self.spray_off_label = "Spray Off"

		#Hotplate Control
		self.on_button = QtWidgets.QPushButton("ON")
		self.off_button = QtWidgets.QPushButton("OFF")
		self.current_temp = QtWidgets.QLCDNumber()
		
		self.on_button.clicked.connect(self.heat_on)
		self.off_button.clicked.connect(self.heat_off)


		#Quadrant 1: matplotlib widget and object
		self.mpl_widget = QtWidgets.QWidget()
		self.mpl = MplCanvas(self.mpl_widget)
		self.mpl_widget.setMinimumHeight(380)

		#Quadrant 2: spray options
		self.spray_options_box = QtWidgets.QGroupBox("Spray Options")
		self.spray_options_layout = QtWidgets.QVBoxLayout()
		self.spray_options_layout.addWidget(self.on_button)
		self.spray_options_layout.addWidget(self.off_button)
		self.spray_options_layout.addWidget(self.current_temp)
		self.spray_options_box.setLayout(self.spray_options_layout)

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
		self.current_temp.display(float(temp))
		self.time.append(self.time[-1]+(self.interval/1000.0))
		self.temp.append(temp)
		self.mpl.update_figure(self.time,self.temp)
		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)

	window.show()
	sys.exit(app.exec_())
