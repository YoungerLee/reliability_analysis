from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex, Qt, pyqtSignal
from PyQt5.QtSql import QSqlQuery
from meta.device import Device

headerIndex = [STATUS, ID, NAME, NUM] = range(4)
headerData = ['全选', '序号', '设备名称', '设备型号']


class DeviceModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        super(DeviceModel, self).__init__(parent)
        self.query = QSqlQuery()
        self.dirty = False
        self.devices = []
        self.checkList = []

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == STATUS:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        if index.column() == ID:
            return ~(Qt.ItemIsEditable | Qt.ItemIsSelectable)
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable | Qt.ItemIsSelectable)

    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
                not (0 <= index.row() < len(self.devices))):
            return QVariant()
        row = index.row()
        column = index.column()
        device = self.devices[row]
        if role == Qt.DisplayRole:
            if column == ID:
                return device.id
            elif column == NAME:
                return device.name
            elif column == NUM:
                return device.num
        elif role == Qt.CheckStateRole:
            if column == STATUS:
                return Qt.Checked if self.checkList[row] == 'Checked' else Qt.Unchecked
        elif role == Qt.ToolTipRole:
            if column == STATUS:
                return self.checkList[row]
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignCenter | Qt.AlignVCenter))
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignCenter | Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight | Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == STATUS:
                    return QVariant(headerData[STATUS])
                elif section == ID:
                    return QVariant(headerData[ID])
                elif section == NAME:
                    return QVariant(headerData[NAME])
                elif section == NUM:
                    return QVariant(headerData[NUM])

    def rowCount(self, index=QModelIndex()):
        return len(self.devices)

    def columnCount(self, index=QModelIndex()):
        return len(headerIndex)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.devices):
            row = index.row()
            column = index.column()
            device = self.devices[row]
            if column == ID:
                device.id = int(value)
            elif column == NAME:
                device.name = str(value)
            elif column == NUM:
                device.num = str(value)
            if role == Qt.CheckStateRole and column == STATUS:
                self.checkList[row] = 'Checked' if value == Qt.Checked else 'Unchecked'
            self.dirty = True
            self.dataChanged[QModelIndex, QModelIndex].emit(index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row, Device())
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.devices = (self.devices[:position] +
                        self.devices[position + rows:])
        self.endRemoveRows()
        self.dirty = True
        return True

    def setHeaderName(self):
        for idx in range(len(headerIndex)):
            self.setHeaderData(headerIndex[idx], Qt.Horizontal, QVariant(headerData[idx]))

    def headerClick(self, isOn):
        self.beginResetModel()
        if isOn:
            self.checkList = ['Checked'] * self.rowCount()
        else:
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()

    def getDeviceByPages(self, limit_index, page_count, fuzzy=''):
        self.beginResetModel()
        self.devices.clear()
        fuzzy_word = fuzzy if fuzzy == '' else "WHERE name LIKE '{0}'".format('%' + fuzzy + '%')
        query_sql = "SELECT * FROM device {2} LIMIT {0}, {1}".format(limit_index, page_count, fuzzy_word)
        self.query.prepare(query_sql)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                device = Device()
                device.id = int(self.query.value(0))
                device.num = str(self.query.value(1))
                device.name = str(self.query.value(2))
                self.devices.append(device)
            self.devices = sorted(self.devices, key=lambda x: x.id)
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()
        self.dirty = False

    def getTotalRecordCount(self, fuzzy=''):
        total_record = 0
        fuzzy_word = fuzzy if fuzzy == '' else "WHERE name LIKE '{0}'".format('%' + fuzzy + '%')
        query_sql = "SELECT count(*) FROM device {0}".format(fuzzy_word)
        self.query.prepare(query_sql)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            if self.query.next():
                total_record = self.query.value(0)
        return total_record

    def delBatchData(self, rows):
        def delOneRow(id):
            query_sql = 'DELETE FROM device WHERE id = :id'
            self.query.prepare(query_sql)
            self.query.bindValue(':id', id)
            if not self.query.exec_():
                print(self.query.lastError().text())
            else:
                print('deleted!')

        for row in rows:
            id = self.devices[row].id
            delOneRow(id)
        self.devices = [val for idx, val in enumerate(self.devices) if idx not in rows]
        self.checkList = [val for idx, val in enumerate(self.checkList) if idx not in rows]

    def updateData(self, device):
        query_sql = 'UPDATE device SET name = :name, num = :num WHERE id = :id'
        self.query.prepare(query_sql)
        self.query.bindValue(':id', device.id)
        self.query.bindValue(':name', device.name)
        self.query.bindValue(':num', device.num)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            print('updated!')

    def insertDevice(self, device):
        insert_sql = 'insert into device(num, name) values (:num, :name)'
        self.query.prepare(insert_sql)
        self.query.bindValue(':num', device.num)
        self.query.bindValue(':name', device.name)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            print('inserted!')
