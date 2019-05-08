# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addDevice.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addDevDialog(object):
    def setupUi(self, addDevDialog):
        addDevDialog.setObjectName("addDevDialog")
        addDevDialog.resize(379, 301)
        self.gridLayout = QtWidgets.QGridLayout(addDevDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(addDevDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(addDevDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(addDevDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(addDevDialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(addDevDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(addDevDialog)
        self.buttonBox.accepted.connect(addDevDialog.accept)
        self.buttonBox.rejected.connect(addDevDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addDevDialog)

    def retranslateUi(self, addDevDialog):
        _translate = QtCore.QCoreApplication.translate
        addDevDialog.setWindowTitle(_translate("addDevDialog", "添加设备"))
        self.label.setText(_translate("addDevDialog", "设备名称："))
        self.label_2.setText(_translate("addDevDialog", "设备型号："))


