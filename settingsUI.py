# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsUI.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MotorSettings(object):
    def setupUi(self, MotorSettings):
        MotorSettings.setObjectName("MotorSettings")
        MotorSettings.setWindowModality(QtCore.Qt.ApplicationModal)
        MotorSettings.resize(600, 155)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MotorSettings.sizePolicy().hasHeightForWidth())
        MotorSettings.setSizePolicy(sizePolicy)
        MotorSettings.setMinimumSize(QtCore.QSize(600, 155))
        MotorSettings.setMaximumSize(QtCore.QSize(600, 155))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cropped-fav_icon-270x270.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MotorSettings.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(MotorSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(MotorSettings)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.microstepping_Label = QtWidgets.QLabel(MotorSettings)
        self.microstepping_Label.setObjectName("microstepping_Label")
        self.gridLayout.addWidget(self.microstepping_Label, 1, 0, 1, 1)
        self.maxwidth_Edit = QtWidgets.QLineEdit(MotorSettings)
        self.maxwidth_Edit.setMaximumSize(QtCore.QSize(75, 16777215))
        self.maxwidth_Edit.setObjectName("maxwidth_Edit")
        self.gridLayout.addWidget(self.maxwidth_Edit, 2, 1, 1, 1)
        self.delay_Edit = QtWidgets.QLineEdit(MotorSettings)
        self.delay_Edit.setMaximumSize(QtCore.QSize(75, 16777215))
        self.delay_Edit.setObjectName("delay_Edit")
        self.gridLayout.addWidget(self.delay_Edit, 0, 1, 1, 1)
        self.sixteen_microstep = QtWidgets.QRadioButton(MotorSettings)
        self.sixteen_microstep.setObjectName("sixteen_microstep")
        self.gridLayout.addWidget(self.sixteen_microstep, 1, 5, 1, 1)
        self.eight_microstep = QtWidgets.QRadioButton(MotorSettings)
        self.eight_microstep.setObjectName("eight_microstep")
        self.gridLayout.addWidget(self.eight_microstep, 1, 4, 1, 1)
        self.one_microstep = QtWidgets.QRadioButton(MotorSettings)
        self.one_microstep.setObjectName("one_microstep")
        self.gridLayout.addWidget(self.one_microstep, 1, 1, 1, 1)
        self.maxwidth_Label = QtWidgets.QLabel(MotorSettings)
        self.maxwidth_Label.setObjectName("maxwidth_Label")
        self.gridLayout.addWidget(self.maxwidth_Label, 2, 0, 1, 1)
        self.delay_Label = QtWidgets.QLabel(MotorSettings)
        self.delay_Label.setObjectName("delay_Label")
        self.gridLayout.addWidget(self.delay_Label, 0, 0, 1, 1)
        self.two_microstep = QtWidgets.QRadioButton(MotorSettings)
        self.two_microstep.setObjectName("two_microstep")
        self.gridLayout.addWidget(self.two_microstep, 1, 2, 1, 1)
        self.four_microstep = QtWidgets.QRadioButton(MotorSettings)
        self.four_microstep.setObjectName("four_microstep")
        self.gridLayout.addWidget(self.four_microstep, 1, 3, 1, 1)
        self.thirtytwo_microstep = QtWidgets.QRadioButton(MotorSettings)
        self.thirtytwo_microstep.setObjectName("thirtytwo_microstep")
        self.gridLayout.addWidget(self.thirtytwo_microstep, 1, 6, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.settingsButtonBox = QtWidgets.QDialogButtonBox(MotorSettings)
        self.settingsButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.settingsButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.settingsButtonBox.setCenterButtons(False)
        self.settingsButtonBox.setObjectName("settingsButtonBox")
        self.horizontalLayout.addWidget(self.settingsButtonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MotorSettings)
        self.settingsButtonBox.accepted.connect(MotorSettings.accept)
        self.settingsButtonBox.rejected.connect(MotorSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(MotorSettings)

    def retranslateUi(self, MotorSettings):
        _translate = QtCore.QCoreApplication.translate
        MotorSettings.setWindowTitle(_translate("MotorSettings", "Sprayer Settings"))
        self.label_4.setText(_translate("MotorSettings", "(200-500)"))
        self.microstepping_Label.setText(_translate("MotorSettings", "Microstepping"))
        self.sixteen_microstep.setText(_translate("MotorSettings", "1/16"))
        self.eight_microstep.setText(_translate("MotorSettings", "1/8"))
        self.one_microstep.setText(_translate("MotorSettings", "1/1"))
        self.maxwidth_Label.setText(_translate("MotorSettings", "Track Length (inches)"))
        self.delay_Label.setText(_translate("MotorSettings", "Motor Delay (microsec)"))
        self.two_microstep.setText(_translate("MotorSettings", "1/2"))
        self.four_microstep.setText(_translate("MotorSettings", "1/4"))
        self.thirtytwo_microstep.setText(_translate("MotorSettings", "1/32"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MotorSettings = QtWidgets.QDialog()
    ui = Ui_MotorSettings()
    ui.setupUi(MotorSettings)
    MotorSettings.show()
    sys.exit(app.exec_())

