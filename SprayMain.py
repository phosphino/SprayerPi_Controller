import sys
from sprayUI import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
from pyqtMpl import *
from pyqtTemp import *

class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)

		self.interval = 1500
		self.timer = QtCore.QTimer()

		self.time = [0]
		self.temp = [0.1]

		#Quadrant 1: matplotlib widget and object
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
		
		self.set_sprayspeed_label = QtWidgets.QLabel("Move Speed: ")
		self.set_sprayspeed_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_sprayspeed_label, self.set_sprayspeed_edit])
		
		self.set_spraypause_label = QtWidgets.QLabel("Pause time (sec): ")
		self.set_spraypause_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spraypause_label, self.set_spraypause_edit])

		self.spray_choice_box = QtWidgets.QGroupBox("Select Spray Mode")
		hbox = QtWidgets.QHBoxLayout()
		self.pneumatic_selection = QtWidgets.QRadioButton("Pneumatic")
		self.pneumatic_selection.setChecked(False)
		self.ultrasonic_selection = QtWidgets.QRadioButton("Ultrasonic")
		self.ultrasonic_selection.setChecked(True)
		hbox.addWidget(self.pneumatic_selection)
		hbox.addWidget(self.ultrasonic_selection)
		self.spray_choice_box.setLayout(hbox)
		self.spray_choice_box.setMaximumHeight(50)
		sprayoptions.append([self.spray_choice_box])

		
		self.loaded_profile_label = QtWidgets.QLabel("Loaded Profile: ")
		self.loaded_profile_edit = QtWidgets.QLabel()

		self.loaded_profile_label.setMaximumHeight(60)
		self.loaded_profile_edit.setMaximumHeight(60)

		self.loaded_profile_label.setMinimumHeight(30)
		self.loaded_profile_edit.setMinimumHeight(30)
		sprayoptions.append([self.loaded_profile_label, self.loaded_profile_edit])
		
		#for loop for putting elements in hbox and adding to vbox
		for x in sprayoptions:
			hbox = QtWidgets.QHBoxLayout()
			for i in x:
				hbox.addWidget(i)
			self.spray_options_layout.addLayout(hbox)	
		
		self.spray_options_box.setLayout(self.spray_options_layout)



		#Quadrant 3: spray_control
		self.spray_control_box = QtWidgets.QGroupBox("Spray Control")
		self.spray_control_layout = QtWidgets.QVBoxLayout()
		
		controloptions = []
		
		self.heating_status = QtWidgets.QLabel("Heating Off")
		controloptions.append([self.heating_status])		
		
		self.spraying_status = QtWidgets.QLabel("Spraying Off")
		controloptions.append([self.spraying_status])
		
		self.spray_number_label = QtWidgets.QLabel("Spray Number: ")
		self.spray_number = QtWidgets.QLabel("0/0")		
		controloptions.append([self.spray_number_label, self.spray_number])
		
		self.run_button = QtWidgets.QPushButton("&Run")
		controloptions.append([self.run_button])
		
		self.stop_button = QtWidgets.QPushButton("&Stop")
		controloptions.append([self.stop_button])
		
		for x in controloptions:
			hbox = QtWidgets.QHBoxLayout()
			for i in x:
				hbox.addWidget(i)
			self.spray_control_layout.addLayout(hbox)
		
		self.spray_control_box.setLayout(self.spray_control_layout)

		#Quadrant 4: spray_progress
		self.spray_progress_layout = QtWidgets.QVBoxLayout()


		#Setup Layout
		self.main_grid = QtWidgets.QGridLayout(self.centralwidget)
		#Adjusting Box Dimensions
		self.mpl_box.setMinimumHeight(50)
		self.mpl_box.setMaximumHeight(300)
		self.mpl_box.setMinimumWidth(400)
		self.main_grid.addWidget(self.mpl_box, 0, 1)

		self.main_grid.addWidget(self.spray_options_box, 0, 0)
		self.spray_options_box.setMaximumWidth(300)
		self.spray_options_box.setMinimumWidth(300)

		self.main_grid.addWidget(self.spray_control_box,1, 0, 1, 1)
		
		#Connect QTimer for Updating
		self.timer.start(self.interval)
		self.timer.timeout.connect(self.update_plot)

	def update_plot(self):
		self.time.append(self.time[-1]+1)
		self.temp.append(self.time[-1]*self.temp[-1])
		self.mpl.update_figure(self.time, self.temp)
		self.temp_lcd.display(self.temp[-1])

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)

	window.show()
	sys.exit(app.exec_())
	
