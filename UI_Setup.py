from PyQt5 import QtCore, QtWidgets, QtGui
from pyqtMpl import *

class UI_Setup(object):
	def __init__(self):
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

		self.mode_label = QtWidgets.QLabel("Mode Selected (Pneumatic or Ultrasonic): ")
		self.mode_selected_label = QtWidgets.QLabel('None Selected')
		sprayoptions.append([self.mode_label, self.mode_selected_label])

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

		


		# for loop for putting elements in hbox and adding to vbox
		j = 0
		i = 0
		for z in range(len(sprayoptions)):
			hbox = QtWidgets.QHBoxLayout()
			for x in sprayoptions[z]:
				hbox.addWidget(x)
			self.spray_options_layout.addLayout(hbox, j, i)
			print(sprayoptions[0], j, i)
			i = i+1
			if i > 2:
				i = 0
				j = j + 1

		self.spray_options_box.setLayout(self.spray_options_layout)
		#self.spray_options_box.setMaximumWidth(300)

		#self.spray_options_box.setMaximumHeight(200)

	def setup_mainscreen(self, centralwidget):
		#Setup Layout
		self.main_grid = QtWidgets.QGridLayout(centralwidget)
		self.main_grid.addWidget(self.mpl_box, 0, 0)
		self.main_grid.addWidget(self.spray_options_box, 1, 0)
