import sys
from sprayUI import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
from pyqtMpl import *


class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)

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


		#Quadrant 1: matplotlib widget and object
		self.mpl_widget = QtWidgets.QWidget()
		self.mpl = MplCanvas(self.mpl_widget)

		#Quadrant 2: spray options
		self.spray_options_box = QtWidgets.QGroupBox("Spray Options")
		self.spray_options_layout = QtWidgets.QVBoxLayout()
		self.spray_options_layout.addWidget(self.on_button)
		self.spray_options_layout.addWidget(self.off_button)
		self.spray_options_layout.addWidget(self.current_temp)
		self.spray_options_box.setLayout(self.spray_options_layout)

		#Quadrant 3: spray_control
		self.spray_control_layout = QtWidgets.QVBoxLayout()

		#Quadrant 4: spray_progress
		self.spray_progress_layout = QtWidgets.QVBoxLayout()


		#Setup Layout
		self.main_grid = QtWidgets.QGridLayout(self.centralwidget)
		self.main_grid.addWidget(self.mpl_widget, 0, 0)
		self.main_grid.addWidget(self.spray_options_box, 1, 0)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)

	window.show()
	sys.exit(app.exec_())