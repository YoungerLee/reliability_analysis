# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'device_list.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_manaDevWidget(object):
    def setupUi(self, manaDevWidget):
        manaDevWidget.setObjectName("manaDevWidget")
        manaDevWidget.resize(967, 676)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(manaDevWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prevButton = QtWidgets.QPushButton(manaDevWidget)
        self.prevButton.setObjectName("prevButton")
        self.horizontalLayout.addWidget(self.prevButton)
        self.nextButton = QtWidgets.QPushButton(manaDevWidget)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        self.switchPageLabel = QtWidgets.QLabel(manaDevWidget)
        self.switchPageLabel.setObjectName("switchPageLabel")
        self.horizontalLayout.addWidget(self.switchPageLabel)
        self.switchPageLineEdit = QtWidgets.QLineEdit(manaDevWidget)
        self.switchPageLineEdit.setMinimumSize(QtCore.QSize(40, 0))
        self.switchPageLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.switchPageLineEdit.setObjectName("switchPageLineEdit")
        self.horizontalLayout.addWidget(self.switchPageLineEdit)
        self.pageLabel = QtWidgets.QLabel(manaDevWidget)
        self.pageLabel.setObjectName("pageLabel")
        self.horizontalLayout.addWidget(self.pageLabel)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.switchPageButton = QtWidgets.QPushButton(manaDevWidget)
        self.switchPageButton.setObjectName("switchPageButton")
        self.horizontalLayout_2.addWidget(self.switchPageButton)
        spacerItem = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.addDevButton = QtWidgets.QPushButton(manaDevWidget)
        self.addDevButton.setObjectName("addDevButton")
        self.horizontalLayout_2.addWidget(self.addDevButton)
        self.updateButton = QtWidgets.QPushButton(manaDevWidget)
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_2.addWidget(self.updateButton)
        self.delBatchButton = QtWidgets.QPushButton(manaDevWidget)
        self.delBatchButton.setObjectName("delBatchButton")
        self.horizontalLayout_2.addWidget(self.delBatchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(528, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.searchEdit = QtWidgets.QLineEdit(manaDevWidget)
        self.searchEdit.setObjectName("searchEdit")
        self.horizontalLayout_3.addWidget(self.searchEdit)
        self.searchButton = QtWidgets.QPushButton(manaDevWidget)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_3.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableView = QtWidgets.QTableView(manaDevWidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(manaDevWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.totalPagesLabel = QtWidgets.QLabel(manaDevWidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.totalPagesLabel.setFont(font)
        self.totalPagesLabel.setObjectName("totalPagesLabel")
        self.horizontalLayout_4.addWidget(self.totalPagesLabel)
        self.pageLabel_2 = QtWidgets.QLabel(manaDevWidget)
        self.pageLabel_2.setObjectName("pageLabel_2")
        self.horizontalLayout_4.addWidget(self.pageLabel_2)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(manaDevWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.currPageLabel = QtWidgets.QLabel(manaDevWidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.currPageLabel.setFont(font)
        self.currPageLabel.setObjectName("currPageLabel")
        self.horizontalLayout_5.addWidget(self.currPageLabel)
        self.pageLabel_3 = QtWidgets.QLabel(manaDevWidget)
        self.pageLabel_3.setObjectName("pageLabel_3")
        self.horizontalLayout_5.addWidget(self.pageLabel_3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        spacerItem2 = QtWidgets.QSpacerItem(618, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(manaDevWidget)
        QtCore.QMetaObject.connectSlotsByName(manaDevWidget)

    def retranslateUi(self, manaDevWidget):
        _translate = QtCore.QCoreApplication.translate
        manaDevWidget.setWindowTitle(_translate("manaDevWidget", "设备列表"))
        self.prevButton.setText(_translate("manaDevWidget", "上一页"))
        self.nextButton.setText(_translate("manaDevWidget", "下一页"))
        self.switchPageLabel.setText(_translate("manaDevWidget", "转到第"))
        self.pageLabel.setText(_translate("manaDevWidget", "页"))
        self.switchPageButton.setText(_translate("manaDevWidget", "Go"))
        self.addDevButton.setText(_translate("manaDevWidget", "添加设备"))
        self.updateButton.setText(_translate("manaDevWidget", "提交修改"))
        self.delBatchButton.setText(_translate("manaDevWidget", "批量删除"))
        self.searchButton.setText(_translate("manaDevWidget", "搜索"))
        self.label_3.setText(_translate("manaDevWidget", "总共"))
        self.totalPagesLabel.setText(_translate("manaDevWidget", "0"))
        self.pageLabel_2.setText(_translate("manaDevWidget", "页"))
        self.label_6.setText(_translate("manaDevWidget", "当前第"))
        self.currPageLabel.setText(_translate("manaDevWidget", "0"))
        self.pageLabel_3.setText(_translate("manaDevWidget", "页"))


