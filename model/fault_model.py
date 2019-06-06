from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex, Qt, pyqtSignal
from PyQt5.QtSql import QSqlQuery
from meta.fault import Fault

headerIndex = [STATUS, ID, PATTERN, POSITION, REASON, ROOT, SITUATION, RECORD_TIME] = range(8)

headerData = ['全选', '序号', '故障模式', '故障部位', '故障原因', '故障溯源', '整机/子系统', '记录时间']

class FaultModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        super(FaultModel, self).__init__(parent)
        self.query = QSqlQuery()
        self.dirty = False
        self.faults = []
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
                not (0 <= index.row() < len(self.faults))):
            return QVariant()
        row = index.row()
        column = index.column()
        fault = self.faults[row]
        if role == Qt.DisplayRole:
            if column == ID:
                return fault.id
            elif column == PATTERN:
                return fault.pattern
            elif column == POSITION:
                return fault.position
            elif column == REASON:
                return fault.reason
            elif column == ROOT:
                return fault.root
            elif column == SITUATION:
                return fault.status
            elif column == RECORD_TIME:
                return fault.record_time
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
                elif section == PATTERN:
                    return QVariant(headerData[PATTERN])
                elif section == POSITION:
                    return QVariant(headerData[POSITION])
                elif section == REASON:
                    return QVariant(headerData[REASON])
                elif section == ROOT:
                    return QVariant(headerData[ROOT])
                elif section == SITUATION:
                    return QVariant(headerData[SITUATION])
                elif section == RECORD_TIME:
                    return QVariant(headerData[RECORD_TIME])

    def rowCount(self, index=QModelIndex()):
        return len(self.faults)

    def columnCount(self, index=QModelIndex()):
        return len(headerIndex)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.faults):
            row = index.row()
            column = index.column()
            fault = self.faults[row]
            if column == ID:
                fault.id = int(value)
            elif column == PATTERN:
                fault.pattern = str(value)
            elif column == POSITION:
                fault.position = str(value)
            elif column == REASON:
                fault.reason = str(value)
            elif column == ROOT:
                fault.root = str(value)
            elif column == SITUATION:
                fault.status = int(value)
            elif column == RECORD_TIME:
                fault.record_time = str(value)
            if role == Qt.CheckStateRole and column == STATUS:
                self.checkList[row] = 'Checked' if value == Qt.Checked else 'Unchecked'
            self.dirty = True
            self.dataChanged[QModelIndex, QModelIndex].emit(index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row, Fault())
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.faults = (self.faults[:position] + self.faults[position + rows:])
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
        self.faults.clear()
        query_sql = 'SELECT id, pattern, position, reason, root, status, record_time FROM breakdown WHERE dev_id = :dev_id'
        self.query.prepare(query_sql)
        self.query.bindValue(':dev_id', dev_id)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                fault = Fault()
                fault.id = int(self.query.value(0))
                fault.pattern = str(self.query.value(1))
                fault.position = str(self.query.value(2))
                fault.reason = str(self.query.value(3))
                fault.root = str(self.query.value(4))
                fault.status = int(self.query.value(5))
                fault.record_time = str(self.query.value(6))
                self.faults.append(fault)
            self.faults = sorted(self.faults, key=lambda x: x.id)
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()
        self.dirty = False

    def delBatchData(self, rows):
        def delOneRow(query, id):
            query_sql = 'DELETE FROM breakdown WHERE id = :id'
            query.prepare(query_sql)
            query.bindValue(':id', id)
            if not query.exec_():
                print(query.lastError().text())
            else:
                print('deleted!')

        for row in rows:
            rec_id = self.faults[row].id
            delOneRow(self.query, rec_id)
        self.faults = [val for idx, val in enumerate(self.faults) if idx not in rows]
        self.checkList = [val for idx, val in enumerate(self.checkList) if idx not in rows]

    def updateData(self, fault):
        query_sql = 'UPDATE breakdown SET pattern = :pattern, position = :position, reason = :reason, root = :root, status = :status WHERE id = :id'
        self.query.prepare(query_sql)
        self.query.bindValue(':id', fault.id)
        self.query.bindValue(':pattern', fault.pattern)
        self.query.bindValue(':position', fault.position)
        self.query.bindValue(':reason', fault.reason)
        self.query.bindValue(':root', fault.root)
        self.query.bindValue(':status', fault.status)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            print('updated!')

    def getTotalRecordCount(self, dev_id, begin_date='', end_date=''):
        total_fault = 0
        query_sql = 'SELECT count(*) FROM breakdown WHERE dev_id = :dev_id'
        if begin_date != '' and end_date != '':
            query_sql += " AND record_time >= '{0}' AND record_time <= '{1}'".format(begin_date, end_date)
        self.query.prepare(query_sql)
        self.query.bindValue(':dev_id', dev_id)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            if self.query.next():
                total_fault = self.query.value(0)
        return total_fault

    def getRecordByDevIdAndPages(self, dev_id, limit_index=0, page_count=10, begin_date='', end_date=''):
        self.beginResetModel()
        self.faults.clear()
        date_query = '' if begin_date == '' or end_date == '' else "AND record_time >= '{0}' AND record_time <= '{1}'".format(
            begin_date, end_date)
        query_sql = 'SELECT id, pattern, position, reason, root, status, record_time FROM breakdown WHERE dev_id = {0} {3} LIMIT {1}, {2}'.format(
            dev_id, limit_index, page_count, date_query)
        self.query.prepare(query_sql)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                fault = Fault()
                fault.id = int(self.query.value(0))
                fault.pattern = str(self.query.value(1))
                fault.position = str(self.query.value(2))
                fault.reason = str(self.query.value(3))
                fault.root = str(self.query.value(4))
                fault.status = int(self.query.value(5))
                fault.record_time = str(self.query.value(6))
                self.faults.append(fault)
            self.faults = sorted(self.faults, key=lambda x: x.id)
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()
        self.dirty = False

    def insertRecord(self, fault, dev_id):
        insert_sql = 'insert into breakdown (pattern, position, reason, root, status, dev_id) values ' \
                     '(:pattern, :position, :reason, :root, :status, :dev_id)'
        self.query.prepare(insert_sql)
        self.query.bindValue(':pattern', fault.pattern)
        self.query.bindValue(':position', fault.position)
        self.query.bindValue(':reason', fault.reason)
        self.query.bindValue(':root', fault.root)
        self.query.bindValue(':status', fault.status)
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
