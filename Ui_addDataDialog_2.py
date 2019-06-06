# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addDataDialog_2.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addDataDialog_2(object):
    def setupUi(self, addDataDialog_2):
        addDataDialog_2.setObjectName("addDataDialog_2")
        addDataDialog_2.resize(692, 527)
        self.gridLayout = QtWidgets.QGridLayout(addDataDialog_2)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(addDataDialog_2)
        self.label.setMinimumSize(QtCore.QSize(162, 0))
        self.label.setMaximumSize(QtCore.QSize(162, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(addDataDialog_2)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(addDataDialog_2)
        self.label_2.setMinimumSize(QtCore.QSize(162, 0))
        self.label_2.setMaximumSize(QtCore.QSize(162, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(addDataDialog_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(addDataDialog_2)
        self.label_3.setMinimumSize(QtCore.QSize(162, 0))
        self.label_3.setMaximumSize(QtCore.QSize(162, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.dateEdit = QtWidgets.QDateEdit(addDataDialog_2)
        self.dateEdit.setObjectName("dateEdit")
        self.horizontalLayout_3.addWidget(self.dateEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(addDataDialog_2)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(addDataDialog_2)
        self.buttonBox.accepted.connect(addDataDialog_2.accept)
        self.buttonBox.rejected.connect(addDataDialog_2.reject)
        QtCore.QMetaObject.connectSlotsByName(addDataDialog_2)

    def retranslateUi(self, addDataDialog_2):
        _translate = QtCore.QCoreApplication.translate
        addDataDialog_2.setWindowTitle(_translate("addDataDialog_2", "添加维修记录"))
        self.label.setText(_translate("addDataDialog_2", "维修日期："))
        self.label_2.setText(_translate("addDataDialog_2", "维修人员："))
        self.label_3.setText(_translate("addDataDialog_2", "维修时间："))


