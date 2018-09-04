import sys
from sprayUI import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
from pyqtMpl import *
#from pyqtTemp import *
from UI_Setup import UI_Setup

class mainwindow(Ui_MainWindow):
	def __init__(self, mainwindow):
		Ui_MainWindow.__init__(self)
		self.setupUi(mainwindow)
		self.UI = UI_Setup()
		self.UI.setup_mainscreen(self.centralwidget)

		x = np.linspace(0,10,1000)
		y = np.sin(x)
		self.UI.mpl.update_figure(x,y)

		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QMainWindow()

	program = mainwindow(window)
	

	window.showMaximized()
	sys.exit(app.exec_())
	
