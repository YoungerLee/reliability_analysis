from Ui_device_list import Ui_manaDevWidget
from Ui_record_list import Ui_manaRecDialog
from Ui_maintain_list import Ui_manaMtDialog
from Ui_fault_list import Ui_manaFaultDialog
from add_data_dialog import *
from model.record_model import *
from model.device_model import *
from model.maintain_model import *
from model.fault_model import *
from utils.table_util import CheckBoxHeader
from utils.valid_utils import *
from PyQt5.QtWidgets import QDialog, QTableView, QApplication, QHeaderView, QMessageBox
from PyQt5.QtCore import pyqtSlot


class DeviceListWidget(QDialog):
    def __init__(self, parent=None):
        super(DeviceListWidget, self).__init__(parent)
        self.ui = Ui_manaDevWidget()
        self.ui.setupUi(self)
        self.__fuzzy = ''
        self.__currentPage = 0  # 当前页
        self.__totalPage = 0  # 总页数
        self.__totalRecordCount = 0  # 总记录数
        self.__pageRecordCount = 10  # 每页显示记录数

        self.model = DeviceModel()
        self.model.setHeaderName()
        self.setTableView()
        self.initFirstPage()

    def setTableView(self):
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setSelectionMode(QTableView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.header = CheckBoxHeader()
        self.header.clicked.connect(self.model.headerClick)
        self.ui.tableView.setHorizontalHeader(self.header)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def initFirstPage(self):
        # 设置当前页
        self.__currentPage = 1
        # 得到总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 得到总页数
        self.__totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 记录查询
        limitIndex = 0
        self.model.getDeviceByPages(limitIndex, self.__pageRecordCount, fuzzy=self.__fuzzy)

    def getTotalRecordCount(self):
        return self.model.getTotalRecordCount(fuzzy=self.__fuzzy)

    def getPageCount(self):
        return int(self.__totalRecordCount / self.__pageRecordCount) \
            if self.__totalRecordCount % self.__pageRecordCount == 0 \
            else int(self.__totalRecordCount / self.__pageRecordCount) + 1

    def updateStatus(self):
        # 设置总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 设置总页数文本
        self.__totalPage = self.getPageCount()
        self.ui.totalPagesLabel.setText(str(self.__totalPage))
        # 设置当前页文本
        self.__currentPage = max(self.__currentPage, 1)
        self.ui.currPageLabel.setText(str(self.__currentPage))
        # 设置按钮是否可用
        if self.__currentPage == 1 and (self.__totalRecordCount == 0 or self.__currentPage == self.__totalPage):
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(False)
        elif self.__currentPage == 1 and self.__currentPage != self.__totalPage:
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(True)
        elif self.__currentPage == self.__totalPage:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(False)
        else:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(True)

    def setTotalPageLabel(self):
        # 设置总页数文本
        self.ui.totalPagesLabel.setText(str(self.__totalPage))

    @pyqtSlot()
    def on_prevButton_clicked(self):
        limitIndex = (self.__currentPage - 2) * self.__pageRecordCount
        self.model.getDeviceByPages(limitIndex, self.__pageRecordCount, fuzzy=self.__fuzzy)
        self.__currentPage -= 1
        self.updateStatus()

    @pyqtSlot()
    def on_nextButton_clicked(self):
        limitIndex = self.__currentPage * self.__pageRecordCount
        self.model.getDeviceByPages(limitIndex, self.__pageRecordCount, fuzzy=self.__fuzzy)
        self.__currentPage += 1
        self.updateStatus()

    def updateThisPage(self):
        limitIndex = (self.__currentPage - 1) * self.__pageRecordCount
        self.model.getDeviceByPages(limitIndex, self.__pageRecordCount, fuzzy=self.__fuzzy)
        self.updateStatus()

    @pyqtSlot()
    def on_switchPageButton_clicked(self):
        # 得到输入字符串
        pgText = self.ui.switchPageLineEdit.text()
        # 判断是否为数字
        if not pgText.isdigit():
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入数字！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 是否为空
        if pgText == None or pgText.strip() == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入跳转页面！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到页数
        pageIndex = int(pgText)
        # 判断是否有指定页
        if pageIndex > self.__totalPage or pageIndex < 1:
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '没有指定页面，请重新输入！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到查询起始行号
        limitIndex = (pageIndex - 1) * self.__pageRecordCount
        # 记录查询
        self.model.getDeviceByPages(limitIndex, self.__pageRecordCount, fuzzy=self.__fuzzy)
        # 设置当前页
        self.__currentPage = pageIndex
        # 刷新状态
        self.updateStatus()

    @pyqtSlot()
    def on_delBatchButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        rows = []
        if reply == QMessageBox.Yes:
            for idx, val in enumerate(self.model.checkList):
                if val == 'Checked':
                    rows.append(idx)
            self.model.delBatchData(rows)
            if self.model.rowCount() <= 0:
                self.on_prevButton_clicked()
                self.header.isOn = False
            else:
                self.updateThisPage()
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '删除成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()

    @pyqtSlot()
    def on_updateButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确认提交修改？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        row = self.ui.tableView.currentIndex().row()
        device = Device(id=self.ui.tableView.model().index(row, ID).data(),
                        name=self.ui.tableView.model().index(row, NAME).data(),
                        num=self.ui.tableView.model().index(row, NUM).data())
        if reply == QMessageBox.Yes:
            self.model.updateData(device)
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '修改成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.updateThisPage()

    @pyqtSlot()
    def on_addDevButton_clicked(self):
        dialog = AddDevDialog()
        dialog.show()
        if dialog.exec_():
            name = dialog.get_name()
            num = dialog.get_num()
            device = Device(name=name, num=num)
            self.model.insertDevice(device)
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '添加成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()
        dialog.destroy()
        self.updateThisPage()

    @pyqtSlot()
    def on_searchButton_clicked(self):
        fuzzy = str(self.ui.searchEdit.text()).strip()
        self.__fuzzy = fuzzy
        self.initFirstPage()


class RecordListDialog(QDialog):
    def __init__(self, parent=None):
        super(RecordListDialog, self).__init__(parent)
        self.ui = Ui_manaRecDialog()
        self.ui.setupUi(self)
        self.model = RecordModel()
        self.model.setHeaderName()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setSelectionMode(QTableView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.header = CheckBoxHeader()
        self.header.clicked.connect(self.model.headerClick)
        self.ui.tableView.setHorizontalHeader(self.header)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__begin_date = ''  # 起始日期
        self.__end_date = ''  # 终止日期
        self.__currentPage = 0  # 当前页
        self.__totalPage = 0  # 总页数
        self.__totalRecordCount = 0  # 总记录数
        self.__pageRecordCount = 10  # 每页显示记录数
        self.dev_id = 0  # 记录表所属设备
        self.initDevInfo()
        self.initFirstPage()
        self.ui.devComboBox.currentIndexChanged.connect(self.on_devComboBox_currentIndexChanged)

    def initDevInfo(self):
        dev_names = self.model.getAllDevName()
        for dev_name in dev_names:
            self.ui.devComboBox.addItem(dev_name)

    def getDevIdByName(self, dev_name):
        return self.model.getDevIdByName(dev_name)

    def initFirstPage(self):
        # 设置当前页
        self.__currentPage = 1
        # 得到总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 得到总页数
        self.__totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 记录查询
        limitIndex = 0
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount,
                                            self.__begin_date, self.__end_date)

    def getTotalRecordCount(self):
        return self.model.getTotalRecordCount(self.dev_id, self.__begin_date, self.__end_date)

    def getPageCount(self):
        return int(self.__totalRecordCount / self.__pageRecordCount) \
            if self.__totalRecordCount % self.__pageRecordCount == 0 \
            else int(self.__totalRecordCount / self.__pageRecordCount) + 1

    def updateStatus(self):
        # 设置总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 设置总页数文本
        self.__totalPage = self.getPageCount()
        self.ui.totalPagesLabel.setText(str(self.__totalPage))
        # 设置当前页文本
        self.__currentPage = max(self.__currentPage, 1)
        self.ui.currPageLabel.setText(str(self.__currentPage))
        # 设置按钮是否可用
        if self.__currentPage == 1 and (self.__totalRecordCount == 0 or self.__currentPage == self.__totalPage):
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(False)
        elif self.__currentPage == 1 and self.__currentPage != self.__totalPage:
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(True)
        elif self.__currentPage == self.__totalPage:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(False)
        else:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(True)

    def setTotalPageLabel(self):
        # 设置总页数文本
        self.ui.totalPagesLabel.setText(str(self.__totalPage))

    @pyqtSlot()
    def on_prevButton_clicked(self):
        limitIndex = (self.__currentPage - 2) * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount, self.__begin_date,
                                            self.__end_date)
        self.__currentPage -= 1
        self.updateStatus()

    @pyqtSlot()
    def on_nextButton_clicked(self):
        limitIndex = self.__currentPage * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount, self.__begin_date,
                                            self.__end_date)
        self.__currentPage += 1
        self.updateStatus()

    def updateThisPage(self):
        limitIndex = (self.__currentPage - 1) * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount, self.__begin_date,
                                            self.__end_date)
        self.updateStatus()

    @pyqtSlot()
    def on_switchPageButton_clicked(self):
        # 得到输入字符串
        pgText = self.ui.switchPageLineEdit.text()
        # 判断是否为数字
        if not pgText.isdigit():
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入数字！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 是否为空
        if pgText == None or pgText.strip() == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入跳转页面！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到页数
        pageIndex = int(pgText)
        # 判断是否有指定页
        if pageIndex > self.__totalPage or pageIndex < 1:
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '没有指定页面，请重新输入！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到查询起始行号
        limitIndex = (pageIndex - 1) * self.__pageRecordCount
        # 记录查询
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount, self.__begin_date,
                                            self.__end_date)
        # 设置当前页
        self.__currentPage = pageIndex
        # 刷新状态
        self.updateStatus()

    @pyqtSlot()
    def on_delBatchButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        rows = []
        if reply == QMessageBox.Yes:
            for idx, val in enumerate(self.model.checkList):
                if val == 'Checked':
                    rows.append(idx)
            self.model.delBatchData(rows)
            if self.model.rowCount() <= 0:
                self.on_prevButton_clicked()
                self.header.isOn = False
            else:
                self.updateThisPage()
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '删除成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()

    @pyqtSlot()
    def on_updateButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确认提交修改？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        row = self.ui.tableView.currentIndex().row()
        record = Record(id=int(self.ui.tableView.model().index(row, ID).data()),
                        run_time=float(self.ui.tableView.model().index(row, RUN_TIME).data()),
                        env_temp=float(self.ui.tableView.model().index(row, ENV_TEMP).data()),
                        kni_temp=float(self.ui.tableView.model().index(row, KNI_TEMP).data()),
                        rpa=float(self.ui.tableView.model().index(row, RPA).data()),
                        axis=str(self.ui.tableView.model().index(row, AXIS).data()))
        if reply == QMessageBox.Yes:
            self.model.updateData(record)
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '修改成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.updateThisPage()

    def on_devComboBox_currentIndexChanged(self):
        dev_name = self.ui.devComboBox.currentText()
        self.dev_id = self.getDevIdByName(dev_name)
        self.initFirstPage()

    @pyqtSlot()
    def on_addDataButton_clicked(self):
        dialog = AddDataDialog_1()
        dialog.show()
        if dialog.exec_():
            run_time = float(dialog.get_run_time())
            env_temp = float(dialog.get_env_temp())
            kni_temp = float(dialog.get_kni_temp())
            rpa = float(dialog.get_rpa())
            axis = dialog.get_axis()
            test_date = dialog.get_test_date()
            record = Record(run_time=run_time, env_temp=env_temp, kni_temp=kni_temp, rpa=rpa, axis=axis, test_date=test_date)
            dev_id = self.dev_id
            if dev_id > 0:
                self.model.insertRecord(record, dev_id)
                msg_box = QMessageBox(QMessageBox.Information,
                                      '提示',
                                      '添加成功！',
                                      QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Information,
                                      '提示',
                                      '请选择设备！',
                                      QMessageBox.Ok)
                msg_box.exec_()
        dialog.destroy()
        self.updateThisPage()

    @pyqtSlot()
    def on_searchButton_clicked(self):
        begin_date = self.ui.beginDateEdit.text()
        end_date = self.ui.endDateEdit.text()
        if compare_date(begin_date, end_date):  # 日期有效
            self.__begin_date = begin_date
            self.__end_date = end_date
            self.initFirstPage()
        else:
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '终止日期必须不小于起始日期！',
                                  QMessageBox.Ok)
            msg_box.exec_()

    @pyqtSlot()
    def on_allQueryButton_clicked(self):
        self.__begin_date = ''
        self.__end_date = ''
        self.initFirstPage()


class MaintainListDialog(QDialog):
    def __init__(self, parent=None):
        super(MaintainListDialog, self).__init__(parent)
        self.ui = Ui_manaMtDialog()
        self.ui.setupUi(self)
        self.model = MaintainModel()
        self.model.setHeaderName()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setSelectionMode(QTableView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.header = CheckBoxHeader()
        self.header.clicked.connect(self.model.headerClick)
        self.ui.tableView.setHorizontalHeader(self.header)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__begin_date = ''  # 起始日期
        self.__end_date = ''  # 终止日期
        self.__currentPage = 0  # 当前页
        self.__totalPage = 0  # 总页数
        self.__totalRecordCount = 0  # 总记录数
        self.__pageRecordCount = 10  # 每页显示记录数
        self.dev_id = 0  # 记录表所属设备
        self.initDevInfo()
        self.initFirstPage()
        self.ui.devComboBox.currentIndexChanged.connect(self.on_devComboBox_currentIndexChanged)

    def initDevInfo(self):
        dev_names = self.model.getAllDevName()
        for dev_name in dev_names:
            self.ui.devComboBox.addItem(dev_name)

    def getDevIdByName(self, dev_name):
        return self.model.getDevIdByName(dev_name)

    def initFirstPage(self):
        # 设置当前页
        self.__currentPage = 1
        # 得到总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 得到总页数
        self.__totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 记录查询
        limitIndex = 0
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount,
                                            self.__begin_date, self.__end_date)

    def getTotalRecordCount(self):
        return self.model.getTotalRecordCount(self.dev_id, self.__begin_date, self.__end_date)

    def getPageCount(self):
        return int(self.__totalRecordCount / self.__pageRecordCount) \
            if self.__totalRecordCount % self.__pageRecordCount == 0 \
            else int(self.__totalRecordCount / self.__pageRecordCount) + 1

    def updateStatus(self):
        # 设置总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 设置总页数文本
        self.__totalPage = self.getPageCount()
        self.ui.totalPagesLabel.setText(str(self.__totalPage))
        # 设置当前页文本
        self.__currentPage = max(self.__currentPage, 1)
        self.ui.currPageLabel.setText(str(self.__currentPage))
        # 设置按钮是否可用
        if self.__currentPage == 1 and (self.__totalRecordCount == 0 or self.__currentPage == self.__totalPage):
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(False)
        elif self.__currentPage == 1 and self.__currentPage != self.__totalPage:
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(True)
        elif self.__currentPage == self.__totalPage:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(False)
        else:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(True)

    def setTotalPageLabel(self):
        # 设置总页数文本
        self.ui.totalPagesLabel.setText(str(self.__totalPage))

    @pyqtSlot()
    def on_prevButton_clicked(self):
        limitIndex = (self.__currentPage - 2) * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        self.__currentPage -= 1
        self.updateStatus()

    @pyqtSlot()
    def on_nextButton_clicked(self):
        limitIndex = self.__currentPage * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        self.__currentPage += 1
        self.updateStatus()

    def updateThisPage(self):
        limitIndex = (self.__currentPage - 1) * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        self.updateStatus()

    @pyqtSlot()
    def on_switchPageButton_clicked(self):
        # 得到输入字符串
        pgText = self.ui.switchPageLineEdit.text()
        # 判断是否为数字
        if not pgText.isdigit():
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入数字！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 是否为空
        if pgText == None or pgText.strip() == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入跳转页面！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到页数
        pageIndex = int(pgText)
        # 判断是否有指定页
        if pageIndex > self.__totalPage or pageIndex < 1:
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '没有指定页面，请重新输入！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到查询起始行号
        limitIndex = (pageIndex - 1) * self.__pageRecordCount
        # 记录查询
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        # 设置当前页
        self.__currentPage = pageIndex
        # 刷新状态
        self.updateStatus()

    @pyqtSlot()
    def on_delBatchButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        rows = []
        if reply == QMessageBox.Yes:
            for idx, val in enumerate(self.model.checkList):
                if val == 'Checked':
                    rows.append(idx)
            self.model.delBatchData(rows)
            if self.model.rowCount() <= 0:
                self.on_prevButton_clicked()
                self.header.isOn = False
            else:
                self.updateThisPage()
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '删除成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()

    @pyqtSlot()
    def on_updateButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确认提交修改？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        row = self.ui.tableView.currentIndex().row()
        maintain = Maintain(id=int(self.ui.tableView.model().index(row, ID).data()),
                            maintain_date=str(self.ui.tableView.model().index(row, MAINTAIN_DATE).data()),
                            person=str(self.ui.tableView.model().index(row, PERSON).data()),
                            maintain_time=float(self.ui.tableView.model().index(row, MAINTAIN_TIME).data()))
        if reply == QMessageBox.Yes:
            self.model.updateData(maintain)
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '修改成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.updateThisPage()

    def on_devComboBox_currentIndexChanged(self):
        dev_name = self.ui.devComboBox.currentText()
        self.dev_id = self.getDevIdByName(dev_name)
        self.initFirstPage()

    @pyqtSlot()
    def on_addDataButton_clicked(self):
        dialog = AddDataDialog_2()
        dialog.show()
        if dialog.exec_():
            maintain_date = str(dialog.get_maintain_date())
            person = str(dialog.get_maintain_person())
            maintain_time = float(dialog.get_maintain_time())
            dev_id = self.dev_id
            maintain = Maintain(maintain_date=maintain_date, person=person, maintain_time=maintain_time)
            if dev_id > 0:
                self.model.insertRecord(maintain, dev_id)
                msg_box = QMessageBox(QMessageBox.Information,
                                      '提示',
                                      '添加成功！',
                                      QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Information,
                                      '提示',
                                      '请选择设备！',
                                      QMessageBox.Ok)
                msg_box.exec_()
        dialog.destroy()
        self.updateThisPage()

    @pyqtSlot()
    def on_searchButton_clicked(self):
        begin_date = self.ui.beginDateEdit.text()
        end_date = self.ui.endDateEdit.text()
        if compare_date(begin_date, end_date):  # 日期有效
            self.__begin_date = begin_date
            self.__end_date = end_date
            self.initFirstPage()
        else:
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '终止日期必须不小于起始日期！',
                                  QMessageBox.Ok)
            msg_box.exec_()

    @pyqtSlot()
    def on_allQueryButton_clicked(self):
        self.__begin_date = ''
        self.__end_date = ''
        self.initFirstPage()

class FaultListDialog(QDialog):
    def __init__(self, parent=None):
        super(FaultListDialog, self).__init__(parent)
        self.ui = Ui_manaFaultDialog()
        self.ui.setupUi(self)
        self.model = FaultModel()
        self.model.setHeaderName()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setSelectionMode(QTableView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.header = CheckBoxHeader()
        self.header.clicked.connect(self.model.headerClick)
        self.ui.tableView.setHorizontalHeader(self.header)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__begin_date = ''  # 起始日期
        self.__end_date = ''  # 终止日期
        self.__currentPage = 0  # 当前页
        self.__totalPage = 0  # 总页数
        self.__totalRecordCount = 0  # 总记录数
        self.__pageRecordCount = 10  # 每页显示记录数
        self.dev_id = 0  # 记录表所属设备
        self.initDevInfo()
        self.initFirstPage()
        self.ui.devComboBox.currentIndexChanged.connect(self.on_devComboBox_currentIndexChanged)

    def initDevInfo(self):
        dev_names = self.model.getAllDevName()
        for dev_name in dev_names:
            self.ui.devComboBox.addItem(dev_name)

    def getDevIdByName(self, dev_name):
        return self.model.getDevIdByName(dev_name)

    def initFirstPage(self):
        # 设置当前页
        self.__currentPage = 1
        # 得到总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 得到总页数
        self.__totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 记录查询
        limitIndex = 0
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount,
                                            self.__begin_date, self.__end_date)

    def getTotalRecordCount(self):
        return self.model.getTotalRecordCount(self.dev_id, self.__begin_date, self.__end_date)

    def getPageCount(self):
        return int(self.__totalRecordCount / self.__pageRecordCount) \
            if self.__totalRecordCount % self.__pageRecordCount == 0 \
            else int(self.__totalRecordCount / self.__pageRecordCount) + 1

    def updateStatus(self):
        # 设置总记录数
        self.__totalRecordCount = self.getTotalRecordCount()
        # 设置总页数文本
        self.__totalPage = self.getPageCount()
        self.ui.totalPagesLabel.setText(str(self.__totalPage))
        # 设置当前页文本
        self.__currentPage = max(self.__currentPage, 1)
        self.ui.currPageLabel.setText(str(self.__currentPage))
        # 设置按钮是否可用
        if self.__currentPage == 1 and (self.__totalRecordCount == 0 or self.__currentPage == self.__totalPage):
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(False)
        elif self.__currentPage == 1 and self.__currentPage != self.__totalPage:
            self.ui.prevButton.setEnabled(False)
            self.ui.nextButton.setEnabled(True)
        elif self.__currentPage == self.__totalPage:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(False)
        else:
            self.ui.prevButton.setEnabled(True)
            self.ui.nextButton.setEnabled(True)

    def setTotalPageLabel(self):
        # 设置总页数文本
        self.ui.totalPagesLabel.setText(str(self.__totalPage))

    @pyqtSlot()
    def on_prevButton_clicked(self):
        limitIndex = (self.__currentPage - 2) * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        self.__currentPage -= 1
        self.updateStatus()

    @pyqtSlot()
    def on_nextButton_clicked(self):
        limitIndex = self.__currentPage * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        self.__currentPage += 1
        self.updateStatus()

    def updateThisPage(self):
        limitIndex = (self.__currentPage - 1) * self.__pageRecordCount
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        self.updateStatus()

    @pyqtSlot()
    def on_switchPageButton_clicked(self):
        # 得到输入字符串
        pgText = self.ui.switchPageLineEdit.text()
        # 判断是否为数字
        if not pgText.isdigit():
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入数字！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 是否为空
        if pgText == None or pgText.strip() == '':
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '请输入跳转页面！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到页数
        pageIndex = int(pgText)
        # 判断是否有指定页
        if pageIndex > self.__totalPage or pageIndex < 1:
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '没有指定页面，请重新输入！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            return
        # 得到查询起始行号
        limitIndex = (pageIndex - 1) * self.__pageRecordCount
        # 记录查询
        self.model.getRecordByDevIdAndPages(self.dev_id, limitIndex, self.__pageRecordCount)
        # 设置当前页
        self.__currentPage = pageIndex
        # 刷新状态
        self.updateStatus()

    @pyqtSlot()
    def on_delBatchButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        rows = []
        if reply == QMessageBox.Yes:
            for idx, val in enumerate(self.model.checkList):
                if val == 'Checked':
                    rows.append(idx)
            self.model.delBatchData(rows)
            if self.model.rowCount() <= 0:
                self.on_prevButton_clicked()
                self.header.isOn = False
            else:
                self.updateThisPage()
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '删除成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()

    @pyqtSlot()
    def on_updateButton_clicked(self):
        reply = QMessageBox.question(self, '确认', '确认提交修改？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        row = self.ui.tableView.currentIndex().row()
        maintain = Maintain(id=int(self.ui.tableView.model().index(row, ID).data()),
                            maintain_date=str(self.ui.tableView.model().index(row, MAINTAIN_DATE).data()),
                            person=str(self.ui.tableView.model().index(row, PERSON).data()),
                            maintain_time=float(self.ui.tableView.model().index(row, MAINTAIN_TIME).data()))
        if reply == QMessageBox.Yes:
            self.model.updateData(maintain)
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '修改成功！',
                                  QMessageBox.Ok)
            msg_box.exec_()
            self.updateThisPage()

    def on_devComboBox_currentIndexChanged(self):
        dev_name = self.ui.devComboBox.currentText()
        self.dev_id = self.getDevIdByName(dev_name)
        self.initFirstPage()

    @pyqtSlot()
    def on_addDataButton_clicked(self):
        dialog = AddDataDialog_3()
        dialog.show()
        if dialog.exec_():
            pattern = dialog.get_pattern()
            position = dialog.get_position()
            reason = dialog.get_reason()
            root = float(dialog.get_root())
            status = dialog.get_status()
            dev_id = self.dev_id
            fault = Fault(pattern=pattern, position=position, reason=reason, root=root, status=status)
            if dev_id > 0:
                self.model.insertRecord(fault, dev_id)
                msg_box = QMessageBox(QMessageBox.Information,
                                      '提示',
                                      '添加成功！',
                                      QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Information,
                                      '提示',
                                      '请选择设备！',
                                      QMessageBox.Ok)
                msg_box.exec_()
        dialog.destroy()
        self.updateThisPage()

    @pyqtSlot()
    def on_searchButton_clicked(self):
        begin_date = self.ui.beginDateEdit.text()
        end_date = self.ui.endDateEdit.text()
        if compare_date(begin_date, end_date):  # 日期有效
            self.__begin_date = begin_date
            self.__end_date = end_date
            self.initFirstPage()
        else:
            msg_box = QMessageBox(QMessageBox.Information,
                                  '提示',
                                  '终止日期必须不小于起始日期！',
                                  QMessageBox.Ok)
            msg_box.exec_()

    @pyqtSlot()
    def on_allQueryButton_clicked(self):
        self.__begin_date = ''
        self.__end_date = ''
        self.initFirstPage()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = RecordListDialog()
    ui.showMaximized()
    sys.exit(app.exec_())
