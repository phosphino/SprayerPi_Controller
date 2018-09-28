# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sprayUI.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1125, 735)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cropped-fav_icon-270x270.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 420))
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CurrentTemperature_label = QtWidgets.QLabel(self.centralwidget)
        self.CurrentTemperature_label.setMaximumSize(QtCore.QSize(225, 16777215))
        self.CurrentTemperature_label.setObjectName("CurrentTemperature_label")
        self.horizontalLayout.addWidget(self.CurrentTemperature_label)
        self.currentTemp_lcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.currentTemp_lcd.setEnabled(True)
        self.currentTemp_lcd.setMinimumSize(QtCore.QSize(75, 50))
        self.currentTemp_lcd.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(45)
        font.setBold(True)
        font.setWeight(75)
        self.currentTemp_lcd.setFont(font)
        self.currentTemp_lcd.setStyleSheet("color: rgb(164, 0, 0);")
        self.currentTemp_lcd.setFrameShape(QtWidgets.QFrame.Box)
        self.currentTemp_lcd.setFrameShadow(QtWidgets.QFrame.Plain)
        self.currentTemp_lcd.setLineWidth(1)
        self.currentTemp_lcd.setSmallDecimalPoint(False)
        self.currentTemp_lcd.setObjectName("currentTemp_lcd")
        self.horizontalLayout.addWidget(self.currentTemp_lcd)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.hotplateStatus_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setBold(True)
        font.setWeight(75)
        self.hotplateStatus_label.setFont(font)
        self.hotplateStatus_label.setObjectName("hotplateStatus_label")
        self.horizontalLayout.addWidget(self.hotplateStatus_label)
        self.hotplatePercent_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.hotplatePercent_label.setFont(font)
        self.hotplatePercent_label.setObjectName("hotplatePercent_label")
        self.horizontalLayout.addWidget(self.hotplatePercent_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.clearPlot_button = QtWidgets.QPushButton(self.centralwidget)
        self.clearPlot_button.setObjectName("clearPlot_button")
        self.horizontalLayout.addWidget(self.clearPlot_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.sprayMode_label = QtWidgets.QLabel(self.groupBox)
        self.sprayMode_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sprayMode_label.setObjectName("sprayMode_label")
        self.gridLayout.addWidget(self.sprayMode_label, 0, 0, 1, 1)
        self.dispenseVolume_label = QtWidgets.QLabel(self.groupBox)
        self.dispenseVolume_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dispenseVolume_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dispenseVolume_label.setObjectName("dispenseVolume_label")
        self.gridLayout.addWidget(self.dispenseVolume_label, 0, 2, 1, 1)
        self.sprayMode_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.sprayMode_comboBox.setMinimumSize(QtCore.QSize(125, 0))
        self.sprayMode_comboBox.setMaximumSize(QtCore.QSize(125, 16777215))
        self.sprayMode_comboBox.setObjectName("sprayMode_comboBox")
        self.sprayMode_comboBox.addItem("")
        self.sprayMode_comboBox.addItem("")
        self.gridLayout.addWidget(self.sprayMode_comboBox, 0, 1, 1, 1)
        self.sprayWidth_edit = QtWidgets.QLineEdit(self.groupBox)
        self.sprayWidth_edit.setMinimumSize(QtCore.QSize(75, 0))
        self.sprayWidth_edit.setMaximumSize(QtCore.QSize(75, 16777215))
        self.sprayWidth_edit.setObjectName("sprayWidth_edit")
        self.gridLayout.addWidget(self.sprayWidth_edit, 1, 5, 1, 1)
        self.dispenseUnits_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.dispenseUnits_comboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.dispenseUnits_comboBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.dispenseUnits_comboBox.setObjectName("dispenseUnits_comboBox")
        self.dispenseUnits_comboBox.addItem("")
        self.dispenseUnits_comboBox.addItem("")
        self.gridLayout.addWidget(self.dispenseUnits_comboBox, 0, 5, 1, 1)
        self.dispenseUnits_label = QtWidgets.QLabel(self.groupBox)
        self.dispenseUnits_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dispenseUnits_label.setObjectName("dispenseUnits_label")
        self.gridLayout.addWidget(self.dispenseUnits_label, 0, 4, 1, 1)
        self.dispenseVolume_edit = QtWidgets.QLineEdit(self.groupBox)
        self.dispenseVolume_edit.setMinimumSize(QtCore.QSize(125, 0))
        self.dispenseVolume_edit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.dispenseVolume_edit.setObjectName("dispenseVolume_edit")
        self.gridLayout.addWidget(self.dispenseVolume_edit, 0, 3, 1, 1)
        self.setPoint_edit = QtWidgets.QLineEdit(self.groupBox)
        self.setPoint_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.setPoint_edit.setMaximumSize(QtCore.QSize(125, 16777215))
        self.setPoint_edit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.setPoint_edit.setObjectName("setPoint_edit")
        self.gridLayout.addWidget(self.setPoint_edit, 1, 7, 1, 1)
        self.setPoint_label = QtWidgets.QLabel(self.groupBox)
        self.setPoint_label.setObjectName("setPoint_label")
        self.gridLayout.addWidget(self.setPoint_label, 1, 6, 1, 1)
        self.dispenseRate_label = QtWidgets.QLabel(self.groupBox)
        self.dispenseRate_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dispenseRate_label.setObjectName("dispenseRate_label")
        self.gridLayout.addWidget(self.dispenseRate_label, 0, 6, 1, 1)
        self.dispenseRate_edit = QtWidgets.QLineEdit(self.groupBox)
        self.dispenseRate_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.dispenseRate_edit.setMaximumSize(QtCore.QSize(125, 16777215))
        self.dispenseRate_edit.setObjectName("dispenseRate_edit")
        self.gridLayout.addWidget(self.dispenseRate_edit, 0, 7, 1, 1)
        self.rateUnits_label = QtWidgets.QLabel(self.groupBox)
        self.rateUnits_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rateUnits_label.setObjectName("rateUnits_label")
        self.gridLayout.addWidget(self.rateUnits_label, 1, 0, 1, 1)
        self.sprayWidth_label = QtWidgets.QLabel(self.groupBox)
        self.sprayWidth_label.setMinimumSize(QtCore.QSize(150, 0))
        self.sprayWidth_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.sprayWidth_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sprayWidth_label.setObjectName("sprayWidth_label")
        self.gridLayout.addWidget(self.sprayWidth_label, 1, 4, 1, 1)
        self.pause_edit = QtWidgets.QLineEdit(self.groupBox)
        self.pause_edit.setMaximumSize(QtCore.QSize(75, 16777215))
        self.pause_edit.setObjectName("pause_edit")
        self.gridLayout.addWidget(self.pause_edit, 1, 3, 1, 1)
        self.pause_label = QtWidgets.QLabel(self.groupBox)
        self.pause_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pause_label.setObjectName("pause_label")
        self.gridLayout.addWidget(self.pause_label, 1, 2, 1, 1)
        self.rateUnits_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.rateUnits_comboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.rateUnits_comboBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.rateUnits_comboBox.setObjectName("rateUnits_comboBox")
        self.rateUnits_comboBox.addItem("")
        self.rateUnits_comboBox.addItem("")
        self.rateUnits_comboBox.addItem("")
        self.rateUnits_comboBox.addItem("")
        self.gridLayout.addWidget(self.rateUnits_comboBox, 1, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(125, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.loadedProfile_label = QtWidgets.QLabel(self.centralwidget)
        self.loadedProfile_label.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.loadedProfile_label.setFont(font)
        self.loadedProfile_label.setObjectName("loadedProfile_label")
        self.horizontalLayout_4.addWidget(self.loadedProfile_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.hotplate_toggle = QtWidgets.QPushButton(self.centralwidget)
        self.hotplate_toggle.setObjectName("hotplate_toggle")
        self.horizontalLayout_4.addWidget(self.hotplate_toggle)
        spacerItem3 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.startRun_button = QtWidgets.QPushButton(self.centralwidget)
        self.startRun_button.setObjectName("startRun_button")
        self.horizontalLayout_4.addWidget(self.startRun_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1125, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_Profile = QtWidgets.QAction(MainWindow)
        self.actionLoad_Profile.setObjectName("actionLoad_Profile")
        self.actionSave_Profile = QtWidgets.QAction(MainWindow)
        self.actionSave_Profile.setObjectName("actionSave_Profile")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuFile.addAction(self.actionLoad_Profile)
        self.menuFile.addAction(self.actionSave_Profile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spray Pyrolysis Control"))
        self.CurrentTemperature_label.setText(_translate("MainWindow", "Current Temperature (Celsius): "))
        self.label_4.setText(_translate("MainWindow", "Hotplate Status: "))
        self.hotplateStatus_label.setText(_translate("MainWindow", "HOTPLATE OFF"))
        self.hotplatePercent_label.setText(_translate("MainWindow", "(0%)"))
        self.clearPlot_button.setText(_translate("MainWindow", "Clear Temperature Plot"))
        self.groupBox.setTitle(_translate("MainWindow", "Spray Settings"))
        self.sprayMode_label.setText(_translate("MainWindow", "Spray Mode"))
        self.dispenseVolume_label.setText(_translate("MainWindow", "Volume to Dispense"))
        self.sprayMode_comboBox.setItemText(0, _translate("MainWindow", "Pneumatic"))
        self.sprayMode_comboBox.setItemText(1, _translate("MainWindow", "Ultrasonic"))
        self.dispenseUnits_comboBox.setItemText(0, _translate("MainWindow", "milliliters"))
        self.dispenseUnits_comboBox.setItemText(1, _translate("MainWindow", "microliters"))
        self.dispenseUnits_label.setText(_translate("MainWindow", "Volume Units"))
        self.setPoint_label.setText(_translate("MainWindow", "Setpoint (Celsius)"))
        self.dispenseRate_label.setText(_translate("MainWindow", "Dispense Rate"))
        self.rateUnits_label.setText(_translate("MainWindow", "Dispense Rate Units"))
        self.sprayWidth_label.setText(_translate("MainWindow", "Spray Width (inches)"))
        self.pause_label.setText(_translate("MainWindow", "Pause Time (sec)"))
        self.rateUnits_comboBox.setItemText(0, _translate("MainWindow", "milliliters/minute"))
        self.rateUnits_comboBox.setItemText(1, _translate("MainWindow", "milliliters/hour"))
        self.rateUnits_comboBox.setItemText(2, _translate("MainWindow", "microliters/minute"))
        self.rateUnits_comboBox.setItemText(3, _translate("MainWindow", "microliters/hour"))
        self.label.setText(_translate("MainWindow", "Loaded Profile: "))
        self.loadedProfile_label.setText(_translate("MainWindow", "**NO PROFILE LOADED**"))
        self.hotplate_toggle.setText(_translate("MainWindow", "Hotplate ON"))
        self.startRun_button.setText(_translate("MainWindow", "RUN"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionLoad_Profile.setText(_translate("MainWindow", "Load Profile"))
        self.actionSave_Profile.setText(_translate("MainWindow", "Save Profile"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

