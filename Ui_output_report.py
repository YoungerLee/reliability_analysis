# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output_report.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_reportDialog(object):
    def setupUi(self, reportDialog):
        reportDialog.setObjectName("reportDialog")
        reportDialog.resize(555, 320)
        self.verticalLayout = QtWidgets.QVBoxLayout(reportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(reportDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.personEdit = QtWidgets.QLineEdit(reportDialog)
        self.personEdit.setObjectName("personEdit")
        self.gridLayout.addWidget(self.personEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(reportDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pathEdit = QtWidgets.QLineEdit(reportDialog)
        self.pathEdit.setObjectName("pathEdit")
        self.gridLayout.addWidget(self.pathEdit, 1, 1, 1, 1)
        self.chooseFolderButton = QtWidgets.QPushButton(reportDialog)
        self.chooseFolderButton.setObjectName("chooseFolderButton")
        self.gridLayout.addWidget(self.chooseFolderButton, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(reportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(reportDialog)
        self.buttonBox.accepted.connect(reportDialog.accept)
        self.buttonBox.rejected.connect(reportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(reportDialog)

    def retranslateUi(self, reportDialog):
        _translate = QtCore.QCoreApplication.translate
        reportDialog.setWindowTitle(_translate("reportDialog", "导出报告"))
        self.label.setText(_translate("reportDialog", "测试人员："))
        self.label_2.setText(_translate("reportDialog", "保存路径："))
        self.pathEdit.setText(_translate("reportDialog", "D:/可靠性分析报告"))
        self.chooseFolderButton.setText(_translate("reportDialog", "选择文件夹"))


