# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maintain_list.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_manaMtDialog(object):
    def setupUi(self, manaMtDialog):
        manaMtDialog.setObjectName("manaMtDialog")
        manaMtDialog.resize(1006, 678)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(manaMtDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prevButton = QtWidgets.QPushButton(manaMtDialog)
        self.prevButton.setObjectName("prevButton")
        self.horizontalLayout.addWidget(self.prevButton)
        self.nextButton = QtWidgets.QPushButton(manaMtDialog)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        self.switchPageLabel = QtWidgets.QLabel(manaMtDialog)
        self.switchPageLabel.setObjectName("switchPageLabel")
        self.horizontalLayout.addWidget(self.switchPageLabel)
        self.switchPageLineEdit = QtWidgets.QLineEdit(manaMtDialog)
        self.switchPageLineEdit.setMinimumSize(QtCore.QSize(40, 0))
        self.switchPageLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.switchPageLineEdit.setObjectName("switchPageLineEdit")
        self.horizontalLayout.addWidget(self.switchPageLineEdit)
        self.pageLabel = QtWidgets.QLabel(manaMtDialog)
        self.pageLabel.setObjectName("pageLabel")
        self.horizontalLayout.addWidget(self.pageLabel)
        self.switchPageButton = QtWidgets.QPushButton(manaMtDialog)
        self.switchPageButton.setObjectName("switchPageButton")
        self.horizontalLayout.addWidget(self.switchPageButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.devComboBox = QtWidgets.QComboBox(manaMtDialog)
        self.devComboBox.setObjectName("devComboBox")
        self.devComboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.devComboBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addDataButton = QtWidgets.QPushButton(manaMtDialog)
        self.addDataButton.setObjectName("addDataButton")
        self.horizontalLayout_2.addWidget(self.addDataButton)
        self.updateButton = QtWidgets.QPushButton(manaMtDialog)
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_2.addWidget(self.updateButton)
        self.delBatchButton = QtWidgets.QPushButton(manaMtDialog)
        self.delBatchButton.setObjectName("delBatchButton")
        self.horizontalLayout_2.addWidget(self.delBatchButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.allQueryButton = QtWidgets.QPushButton(manaMtDialog)
        self.allQueryButton.setObjectName("allQueryButton")
        self.horizontalLayout_7.addWidget(self.allQueryButton)
        spacerItem = QtWidgets.QSpacerItem(178, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.label_9 = QtWidgets.QLabel(manaMtDialog)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        self.beginDateEdit = QtWidgets.QDateEdit(manaMtDialog)
        self.beginDateEdit.setObjectName("beginDateEdit")
        self.horizontalLayout_7.addWidget(self.beginDateEdit)
        self.label_10 = QtWidgets.QLabel(manaMtDialog)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.endDateEdit = QtWidgets.QDateEdit(manaMtDialog)
        self.endDateEdit.setObjectName("endDateEdit")
        self.horizontalLayout_7.addWidget(self.endDateEdit)
        self.searchButton = QtWidgets.QPushButton(manaMtDialog)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_7.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.tableView = QtWidgets.QTableView(manaMtDialog)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(manaMtDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.totalPagesLabel = QtWidgets.QLabel(manaMtDialog)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.totalPagesLabel.setFont(font)
        self.totalPagesLabel.setObjectName("totalPagesLabel")
        self.horizontalLayout_4.addWidget(self.totalPagesLabel)
        self.pageLabel_2 = QtWidgets.QLabel(manaMtDialog)
        self.pageLabel_2.setObjectName("pageLabel_2")
        self.horizontalLayout_4.addWidget(self.pageLabel_2)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(manaMtDialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.currPageLabel = QtWidgets.QLabel(manaMtDialog)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.currPageLabel.setFont(font)
        self.currPageLabel.setObjectName("currPageLabel")
        self.horizontalLayout_5.addWidget(self.currPageLabel)
        self.pageLabel_3 = QtWidgets.QLabel(manaMtDialog)
        self.pageLabel_3.setObjectName("pageLabel_3")
        self.horizontalLayout_5.addWidget(self.pageLabel_3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(618, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(manaMtDialog)
        QtCore.QMetaObject.connectSlotsByName(manaMtDialog)

    def retranslateUi(self, manaMtDialog):
        _translate = QtCore.QCoreApplication.translate
        manaMtDialog.setWindowTitle(_translate("manaMtDialog", "维修记录列表"))
        self.prevButton.setText(_translate("manaMtDialog", "上一页"))
        self.nextButton.setText(_translate("manaMtDialog", "下一页"))
        self.switchPageLabel.setText(_translate("manaMtDialog", "转到第"))
        self.pageLabel.setText(_translate("manaMtDialog", "页"))
        self.switchPageButton.setText(_translate("manaMtDialog", "Go"))
        self.devComboBox.setItemText(0, _translate("manaMtDialog", "选择设备"))
        self.addDataButton.setText(_translate("manaMtDialog", "添加记录"))
        self.updateButton.setText(_translate("manaMtDialog", "提交修改"))
        self.delBatchButton.setText(_translate("manaMtDialog", "批量删除"))
        self.allQueryButton.setText(_translate("manaMtDialog", "全部记录"))
        self.label_9.setText(_translate("manaMtDialog", "起始日期："))
        self.label_10.setText(_translate("manaMtDialog", "终止日期："))
        self.searchButton.setText(_translate("manaMtDialog", "搜索"))
        self.label_3.setText(_translate("manaMtDialog", "总共"))
        self.totalPagesLabel.setText(_translate("manaMtDialog", "0"))
        self.pageLabel_2.setText(_translate("manaMtDialog", "页"))
        self.label_6.setText(_translate("manaMtDialog", "当前第"))
        self.currPageLabel.setText(_translate("manaMtDialog", "0"))
        self.pageLabel_3.setText(_translate("manaMtDialog", "页"))


