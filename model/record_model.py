from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex, Qt, pyqtSignal
from PyQt5.QtSql import QSqlQuery
from meta.record import Record

headerIndex = [STATUS, ID, RUN_TIME, ENV_TEMP, KNI_TEMP, RPA, AXIS] = range(7)
headerData = ['全选', '序号', '运行时间/h', '环境温度/℃', '刀头温度/℃', '重复定位精度/μm', '轴向']


class RecordModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        super(RecordModel, self).__init__(parent)
        self.query = QSqlQuery()
        self.dirty = False
        self.records = []
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
                not (0 <= index.row() < len(self.records))):
            return QVariant()
        row = index.row()
        column = index.column()
        record = self.records[row]
        if role == Qt.DisplayRole:
            if column == ID:
                return record.id
            elif column == RUN_TIME:
                return record.run_time
            elif column == ENV_TEMP:
                return record.env_temp
            elif column == KNI_TEMP:
                return record.kni_temp
            elif column == RPA:
                return record.rpa
            elif column == AXIS:
                return record.axis
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
                elif section == RUN_TIME:
                    return QVariant(headerData[RUN_TIME])
                elif section == ENV_TEMP:
                    return QVariant(headerData[ENV_TEMP])
                elif section == KNI_TEMP:
                    return QVariant(headerData[KNI_TEMP])
                elif section == RPA:
                    return QVariant(headerData[RPA])
                elif section == AXIS:
                    return QVariant(headerData[AXIS])

    def rowCount(self, index=QModelIndex()):
        return len(self.records)

    def columnCount(self, index=QModelIndex()):
        return len(headerIndex)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.records):
            row = index.row()
            column = index.column()
            record = self.records[row]
            if column == ID:
                record.id = int(value)
            elif column == RUN_TIME:
                record.run_time = float(value)
            elif column == ENV_TEMP:
                record.env_temp = float(value)
            elif column == KNI_TEMP:
                record.kni_temp = float(value)
            elif column == RPA:
                record.rpa = float(value)
            elif column == AXIS:
                record.axis = str(value)
            if role == Qt.CheckStateRole and column == STATUS:
                self.checkList[row] = 'Checked' if value == Qt.Checked else 'Unchecked'
            self.dirty = True
            self.dataChanged[QModelIndex, QModelIndex].emit(index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row, Record())
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = (self.records[:position] +
                        self.records[position + rows:])
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

    def loadRecordDataByDevId(self, dev_id):
        self.beginResetModel()
        self.records.clear()
        query_sql = 'SELECT id, run_time, env_temp, kni_temp, rpa, axis FROM record WHERE dev_id = :dev_id'
        self.query.prepare(query_sql)
        self.query.bindValue(':dev_id', dev_id)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                record = Record()
                record.id = int(self.query.value(0))
                record.run_time = float(self.query.value(1))
                record.env_temp = float(self.query.value(2))
                record.kni_temp = float(self.query.value(3))
                record.rpa = float(self.query.value(4))
                record.axis = str(self.query.value(5))
                self.records.append(record)
            self.records = sorted(self.records, key=lambda x: x.id)
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()
        self.dirty = False

    def delBatchData(self, rows):
        def delOneRow(query, id):
            query_sql = 'DELETE FROM record WHERE id = :id'
            query.prepare(query_sql)
            query.bindValue(':id', id)
            if not query.exec_():
                print(query.lastError().text())
            else:
                print('deleted!')

        for row in rows:
            rec_id = self.records[row].id
            delOneRow(self.query, rec_id)
        self.records = [val for idx, val in enumerate(self.records) if idx not in rows]
        self.checkList = [val for idx, val in enumerate(self.checkList) if idx not in rows]

    def updateData(self, record):
        query_sql = 'UPDATE record SET run_time = :run_time, env_temp = :env_temp, ' \
                    'kni_temp = :kni_temp, rpa = :rpa, axis = :axis WHERE id = :id'
        self.query.prepare(query_sql)
        self.query.bindValue(':id', record.id)
        self.query.bindValue(':run_time', record.run_time)
        self.query.bindValue(':env_temp', record.env_temp)
        self.query.bindValue(':kni_temp', record.kni_temp)
        self.query.bindValue(':rpa', record.rpa)
        self.query.bindValue(':axis', record.axis)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            print('updated!')

    def getTotalRecordCount(self, dev_id):
        total_record = 0
        query_sql = 'SELECT count(*) FROM record WHERE dev_id = :dev_id'
        self.query.prepare(query_sql)
        self.query.bindValue(':dev_id', dev_id)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            if self.query.next():
                total_record = self.query.value(0)
        return total_record

    def getRecordByDevIdAndPages(self, dev_id, limit_index=0, page_count=10):
        self.beginResetModel()
        self.records.clear()
        query_sql = 'SELECT id, run_time, env_temp, kni_temp, rpa, axis FROM record WHERE dev_id = {0} LIMIT {1}, {2}'.format(
            dev_id, limit_index, page_count)
        self.query.prepare(query_sql)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                record = Record()
                record.id = int(self.query.value(0))
                record.run_time = float(self.query.value(1))
                record.env_temp = float(self.query.value(2))
                record.kni_temp = float(self.query.value(3))
                record.rpa = float(self.query.value(4))
                record.axis = str(self.query.value(5))
                self.records.append(record)
            self.records = sorted(self.records, key=lambda x: x.id)
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()
        self.dirty = False

    def insertRecord(self, record, dev_id):
        insert_sql = 'insert into record(run_time, env_temp, kni_temp, rpa, axis, dev_id) values ' \
                     '(:run_time, :env_temp, :kni_temp, :rpa, :axis, :dev_id)'
        self.query.prepare(insert_sql)
        self.query.bindValue(':run_time', record.run_time)
        self.query.bindValue(':env_temp', record.env_temp)
        self.query.bindValue(':kni_temp', record.kni_temp)
        self.query.bindValue(':rpa', record.rpa)
        self.query.bindValue(':axis', record.axis)
        self.query.bindValue(':dev_id', dev_id)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            print('inserted!')

    def getDevIdByName(self, dev_name):
        id = 0
        if dev_name != '选择设备':
            query_sql = 'SELECT id FROM device WHERE name = :name'
            self.query.prepare(query_sql)
            self.query.bindValue(':name', dev_name)
            if not self.query.exec_():
                print(self.query.lastError())
            else:
                while self.query.next():
                    id = self.query.value(0)
        return int(id)

    def getAllDevName(self):
        dev_names = []
        query_sql = 'select name from device'
        self.query.prepare(query_sql)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                name = self.query.value(0)
                dev_names.append(name)
        return dev_names


if __name__ == '__main__':
    model = RecordModel()
    model.loadDeviceData()
    for i in range(len(headerIndex)):
        idx = model.index(0, i)
        print(model.data(idx))
