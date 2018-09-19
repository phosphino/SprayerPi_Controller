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
        MainWindow.resize(1002, 661)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cropped-fav_icon-270x270.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1002, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSelect_Mode = QtWidgets.QMenu(self.menuFile)
        self.menuSelect_Mode.setObjectName("menuSelect_Mode")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_Profile = QtWidgets.QAction(MainWindow)
        self.actionLoad_Profile.setObjectName("actionLoad_Profile")
        self.actionSave_Profile = QtWidgets.QAction(MainWindow)
        self.actionSave_Profile.setObjectName("actionSave_Profile")
        self.actionPneumatic = QtWidgets.QAction(MainWindow)
        self.actionPneumatic.setObjectName("actionPneumatic")
        self.actionUltrasonic = QtWidgets.QAction(MainWindow)
        self.actionUltrasonic.setObjectName("actionUltrasonic")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuSelect_Mode.addAction(self.actionPneumatic)
        self.menuSelect_Mode.addAction(self.actionUltrasonic)
        self.menuFile.addAction(self.actionLoad_Profile)
        self.menuFile.addAction(self.actionSave_Profile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.menuSelect_Mode.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spray Pyrolysis Control"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSelect_Mode.setTitle(_translate("MainWindow", "Select Mode"))
        self.actionLoad_Profile.setText(_translate("MainWindow", "Load Profile"))
        self.actionSave_Profile.setText(_translate("MainWindow", "Save Profile"))
        self.actionPneumatic.setText(_translate("MainWindow", "Pneumatic"))
        self.actionUltrasonic.setText(_translate("MainWindow", "Ultrasonic"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

