'''
Andrew Breuhaus-Alvarez, 2018
Model and Control code for Spray Pyrolysis Control Software
'''
import sys
from sprayUI import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
from pyqtMpl import *
from stepper_control import motorcontrol
from pyqtTemp import *

class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		'''
		POPULATE MAIN WINDOW
		'''
		self.sprayoptions_dict = {}
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
		sprayoptions = []
		self.spray_options_box = QtWidgets.QGroupBox("Spray Options")
		self.spray_options_layout = QtWidgets.QGridLayout(self.spray_options_box)

		self.mode_label = QtWidgets.QLabel("Mode Selected: ")
		self.mode_selected_label = QtWidgets.QLabel('None Selected')
		sprayoptions.append([self.mode_label, self.mode_selected_label])

		self.set_temp_label = QtWidgets.QLabel("Set Point (Celsius): ")
		self.set_temp_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_temp_label, self.set_temp_edit])

		self.set_spray_label = QtWidgets.QLabel("Number of sprays: ")
		self.set_spray_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spray_label, self.set_spray_edit])

		self.set_sprayspeed_label = QtWidgets.QLabel("Move Speed (inch/sec): ")
		self.set_sprayspeed_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_sprayspeed_label, self.set_sprayspeed_edit])
		
		self.set_spray_volume_label = QtWidgets.QLabel("Spray Volume (mL): ")
		self.set_spray_volume_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spray_volume_label, self.set_spray_volume_edit])
		
		self.set_pause_label = QtWidgets.QLabel("Pause time (sec): ")
		self.set_pause_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_pause_label, self.set_pause_edit])
		
		self.set_spray_width_label = QtWidgets.QLabel("Spray Travel Distance (inches): ")
		self.set_spray_width_edit = QtWidgets.QLineEdit()
		sprayoptions.append([self.set_spray_width_label, self.set_spray_width_edit])

		self.loaded_profile_label = QtWidgets.QLabel("Loaded Profile: ")
		self.loaded_profile_edit = QtWidgets.QLabel()
		sprayoptions.append([self.loaded_profile_label, self.loaded_profile_edit])
		
		self.standby_button = QtWidgets.QPushButton("&Standby")
		sprayoptions.append([self.standby_button])

		# for loop for putting elements in hbox and adding to vbox
		j = 0
		i = 0
		for z in range(len(sprayoptions)):
			hbox = QtWidgets.QHBoxLayout()
			for x in sprayoptions[z]:
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
		END POPULATING MAINWINDOW
		'''
		
		#Variables to be used during spraying. Set when standby button pressed
		self.__spray_width = None
		self.__spray_speed = None
		self.__cycles = None
		self.__pause_time = None
		self.__spray_volume = None
			
		

		self.__motor_connect = False
		self.m = motorcontrol()		
		self.standby_button.clicked.connect(self.run_test)

		x = np.linspace(0,10,1000)
		y = np.sin(x)
		self.mpl.update_figure(x,y)
		
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
			error_dialog = QtWidgets.QMessageBox()
			error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
			error_dialog.setText("Input Numeric Values")
			error_dialog.exec_()
		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)
	

	window.showMaximized()
	sys.exit(app.exec_())
	
