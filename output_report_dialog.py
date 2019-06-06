from Ui_output_report import Ui_reportDialog
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSlot
import os
class OutputReportDialog(QDialog):
    def __init__(self, parent=None):
        super(OutputReportDialog, self).__init__(parent)
        self.ui = Ui_reportDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.acceptEvent)
        self.ui.buttonBox.rejected.connect(self.rejectEvent)

    def acceptEvent(self):
        if self.ui.personEdit.text().strip() == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请填写测试人员',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.reject()
        else:
            self.accept()

    def rejectEvent(self):
        self.reject()

    def get_person(self):
        return self.ui.personEdit.text()

    def get_path(self):
        return self.ui.pathEdit.text()

    @pyqtSlot()
    def on_chooseFolderButton_clicked(self):
        save_dir = QFileDialog.getExistingDirectory(self, '选择文件夹', './')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.ui.pathEdit.setText(save_dir)