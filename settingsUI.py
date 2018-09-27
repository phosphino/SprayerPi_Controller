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
        MotorSettings.resize(351, 156)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MotorSettings.sizePolicy().hasHeightForWidth())
        MotorSettings.setSizePolicy(sizePolicy)
        MotorSettings.setMinimumSize(QtCore.QSize(0, 0))
        MotorSettings.setMaximumSize(QtCore.QSize(351, 156))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cropped-fav_icon-270x270.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MotorSettings.setWindowIcon(icon)
        MotorSettings.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout = QtWidgets.QVBoxLayout(MotorSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.delay_edit = QtWidgets.QLineEdit(MotorSettings)
        self.delay_edit.setMaximumSize(QtCore.QSize(75, 16777215))
        self.delay_edit.setObjectName("delay_edit")
        self.gridLayout.addWidget(self.delay_edit, 0, 2, 1, 1)
        self.microstepping_Label = QtWidgets.QLabel(MotorSettings)
        self.microstepping_Label.setObjectName("microstepping_Label")
        self.gridLayout.addWidget(self.microstepping_Label, 1, 0, 1, 1)
        self.maxWidth_label = QtWidgets.QLabel(MotorSettings)
        self.maxWidth_label.setObjectName("maxWidth_label")
        self.gridLayout.addWidget(self.maxWidth_label, 2, 0, 1, 1)
        self.delay_label = QtWidgets.QLabel(MotorSettings)
        self.delay_label.setObjectName("delay_label")
        self.gridLayout.addWidget(self.delay_label, 0, 0, 1, 1)
        self.microstepping_comboBox = QtWidgets.QComboBox(MotorSettings)
        self.microstepping_comboBox.setObjectName("microstepping_comboBox")
        self.microstepping_comboBox.addItem("")
        self.microstepping_comboBox.addItem("")
        self.microstepping_comboBox.addItem("")
        self.microstepping_comboBox.addItem("")
        self.microstepping_comboBox.addItem("")
        self.microstepping_comboBox.addItem("")
        self.gridLayout.addWidget(self.microstepping_comboBox, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(MotorSettings)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.maxWidth_edit = QtWidgets.QLineEdit(MotorSettings)
        self.maxWidth_edit.setMaximumSize(QtCore.QSize(75, 16777215))
        self.maxWidth_edit.setObjectName("maxWidth_edit")
        self.gridLayout.addWidget(self.maxWidth_edit, 2, 2, 1, 1)
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
        MotorSettings.setWindowTitle(_translate("MotorSettings", "Spray Settings"))
        self.microstepping_Label.setText(_translate("MotorSettings", "Microstepping"))
        self.maxWidth_label.setText(_translate("MotorSettings", "Track Length (inches)"))
        self.delay_label.setText(_translate("MotorSettings", "Motor Delay (microsec)"))
        self.microstepping_comboBox.setItemText(0, _translate("MotorSettings", "1/1"))
        self.microstepping_comboBox.setItemText(1, _translate("MotorSettings", "1/2"))
        self.microstepping_comboBox.setItemText(2, _translate("MotorSettings", "1/4"))
        self.microstepping_comboBox.setItemText(3, _translate("MotorSettings", "1/8"))
        self.microstepping_comboBox.setItemText(4, _translate("MotorSettings", "1/16"))
        self.microstepping_comboBox.setItemText(5, _translate("MotorSettings", "1/32"))
        self.label_4.setText(_translate("MotorSettings", "(200-500)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MotorSettings = QtWidgets.QDialog()
    ui = Ui_MotorSettings()
    ui.setupUi(MotorSettings)
    MotorSettings.show()
    sys.exit(app.exec_())

