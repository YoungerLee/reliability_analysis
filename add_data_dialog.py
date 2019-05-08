from Ui_addDataDialog_1 import Ui_addDataDialog
from Ui_addDataDialog_2 import Ui_addDataDialog_2
from Ui_addDataDialog_3 import Ui_addDataDialog_3
from Ui_addDevice import Ui_addDevDialog
from PyQt5.QtWidgets import QDialog, QMessageBox
class AddDataDialog_1(QDialog):
    def __init__(self, parent=None):
        super(AddDataDialog_1, self).__init__(parent)
        self.ui = Ui_addDataDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.acceptEvent)
        self.ui.buttonBox.rejected.connect(self.rejectEvent)

    def acceptEvent(self):
        if self.ui.lineEdit.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写运行时间',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_2.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写环境温度',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_3.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写刀头温度',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_4.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写精度',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        else:
            self.accept()
    def rejectEvent(self):
        self.reject()

    def get_run_time(self):
        return self.ui.lineEdit.text()

    def get_env_temp(self):
        return self.ui.lineEdit_2.text()

    def get_kni_temp(self):
        return self.ui.lineEdit_3.text()

    def get_rpa(self):
        return self.ui.lineEdit_4.text()

    def get_axis(self):
        return self.ui.comboBox.currentText()

class AddDataDialog_2(QDialog):
    def __init__(self, parent=None):
        super(AddDataDialog_2, self).__init__(parent)
        self.ui = Ui_addDataDialog_2()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.acceptEvent)
        self.ui.buttonBox.rejected.connect(self.rejectEvent)
    def acceptEvent(self):
        if self.ui.lineEdit.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写维修日期',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_2.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写维修人员',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_3.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写维修时间',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        else:
            self.accept()
    def rejectEvent(self):
        self.reject()
    def get_maintain_date(self):
        return self.ui.lineEdit.text()

    def get_maintain_person(self):
        return self.ui.lineEdit_2.text()

    def get_maintain_time(self):
        return self.ui.lineEdit_3.text()

class AddDataDialog_3(QDialog):
    def __init__(self, parent=None):
        super(AddDataDialog_3, self).__init__(parent)
        self.ui = Ui_addDataDialog_3()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.acceptEvent)
        self.ui.buttonBox.rejected.connect(self.rejectEvent)

    def acceptEvent(self):
        if self.ui.lineEdit.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写故障模式',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_2.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写故障部位',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_3.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写故障原因',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_4.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写故障溯源',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        else:
            self.accept()
    def rejectEvent(self):
        self.reject()

    def get_pattern(self):
        return self.ui.lineEdit.text()

    def get_position(self):
        return self.ui.lineEdit_2.text()

    def get_reason(self):
        return self.ui.lineEdit_3.text()

    def get_root(self):
        return self.ui.lineEdit_4.text()

    def get_status(self):
        text = self.ui.comboBox.currentText()
        idx = 0
        if text == '整机':
            idx = 1
        else:
            idx = 0
        return idx

class AddDevDialog(QDialog):
    def __init__(self, parent=None):
        super(AddDevDialog, self).__init__(parent)
        self.ui = Ui_addDevDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.acceptEvent)
        self.ui.buttonBox.rejected.connect(self.rejectEvent)

    def acceptEvent(self):
        if self.ui.lineEdit.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写设备名称',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        elif self.ui.lineEdit_2.text().strip(' ') == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写设备型号',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        else:
            self.accept()

    def rejectEvent(self):
        self.reject()

    def get_name(self):
        return self.ui.lineEdit.text()

    def get_num(self):
        return self.ui.lineEdit_2.text()
