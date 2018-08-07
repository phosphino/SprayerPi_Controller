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
		
		self.timer = QtCore.QTimer()
		self.interval = 1500
		print (self.centralwidget.width())
		#GPIO setup
		GPIO.setmode(GPIO.BOARD)#Using Physical Pin Numbers		
		GPIO.setwarnings(False)
		
		#Thermocouple setup
		self.thermocouple = adatemp()
		self.time = [0]
		self.temp = [self.thermocouple.temp()]
		
		self.run_boolean = False
				
		#GPIO setup: Hotplate
		self.gpio_hotplate = 8 #hotplate relay is connected to pin #8 
		GPIO.setup(self.gpio_hotplate, GPIO.OUT, initial=GPIO.LOW)

		#Top Half: matplotlib widget and object
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

		#Bottom Half: spray options
		sprayoptions = []
		self.spray_options_box = QtWidgets.QGroupBox("Spray Options")
		self.spray_options_layout = QtWidgets.QVBoxLayout()
		
		self.set_temp_label = QtWidgets.QLabel("Set Point (Celsius): ")
		self.set_temp_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_temp_label, self.set_temp_edit])
		
		self.set_spray_label = QtWidgets.QLabel("Number of sprays: ")
		self.set_spray_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spray_label, self.set_spray_edit])
		
		self.set_sprayspeed_label = QtWidgets.QLabel("Move Speed: ")
		self.set_sprayspeed_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_sprayspeed_label, self.set_sprayspeed_edit])
		
		self.set_spraypause_label = QtWidgets.QLabel("Pause time (sec): ")
		self.set_spraypause_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spraypause_label, self.set_spraypause_edit])
		
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
		self.spray_options_box.setMaximumWidth(300)
		
		self.spray_options_box.setMaximumHeight(200)

		#Setup Layout
		self.main_grid = QtWidgets.QGridLayout(self.centralwidget)
		self.main_grid.addWidget(self.mpl_box, 0, 0)
		self.main_grid.addWidget(self.spray_options_box, 1, 0)
		
		#Connect QTimer for Updating
		self.timer.timeout.connect(self.update_temperature)
		self.timer.start(self.interval)
		
		#self.run_button.clicked.connect(self.heat_to_setpoint)
		#self.stop_button.clicked.connect(self.heat_off)
				
		
		
	def heat_on(self):
		GPIO.output(self.gpio_hotplate, GPIO.HIGH)
	
	def heat_off(self):
		GPIO.output(self.gpio_hotplate, GPIO.LOW)
		
	def heater_control(self, temp):
		setpoint = float(self.set_temp_edit.text())
		if temp < setpoint:
			pass
	
		
	def update_temperature(self):
		temp = self.thermocouple.temp()
		self.time.append(self.time[-1]+(self.interval/1000.0))
		self.temp.append(temp)
		self.mpl.update_figure(self.time,self.temp)
		self.temp_lcd.display(temp)
		if self.run_boolean == True:
			self.heater_control(temp)
			
			
	def closeEvent(self, event):
		print("CLOSEING")
		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)
	

	window.showMaximized()
	sys.exit(app.exec_())
	
