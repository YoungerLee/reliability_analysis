from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex, Qt, pyqtSignal
from PyQt5.QtSql import QSqlQuery
from meta.maintain import Maintain

headerIndex = [STATUS, ID, MAINTAIN_DATE, PERSON, MAINTAIN_TIME] = range(5)

headerData = ['全选', '序号', '维修日期', '维修人员', '维修时间/h']


class MaintainModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        super(MaintainModel, self).__init__(parent)
        self.query = QSqlQuery()
        self.dirty = False
        self.maintains = []
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
                not (0 <= index.row() < len(self.maintains))):
            return QVariant()
        row = index.row()
        column = index.column()
        maintain = self.maintains[row]
        if role == Qt.DisplayRole:
            if column == ID:
                return maintain.id
            elif column == MAINTAIN_DATE:
                return maintain.maintain_date
            elif column == PERSON:
                return maintain.person
            elif column == MAINTAIN_TIME:
                return maintain.maintain_time
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
                elif section == MAINTAIN_DATE:
                    return QVariant(headerData[MAINTAIN_DATE])
                elif section == PERSON:
                    return QVariant(headerData[PERSON])
                elif section == MAINTAIN_TIME:
                    return QVariant(headerData[MAINTAIN_TIME])

    def rowCount(self, index=QModelIndex()):
        return len(self.maintains)

    def columnCount(self, index=QModelIndex()):
        return len(headerIndex)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.maintains):
            row = index.row()
            column = index.column()
            maintain = self.maintains[row]
            if column == ID:
                maintain.id = int(value)
            elif column == MAINTAIN_DATE:
                maintain.maintain_date = str(value)
            elif column == PERSON:
                maintain.person = str(value)
            elif column == MAINTAIN_TIME:
                maintain.maintain_time = float(value)
            if role == Qt.CheckStateRole and column == STATUS:
                self.checkList[row] = 'Checked' if value == Qt.Checked else 'Unchecked'
            self.dirty = True
            self.dataChanged[QModelIndex, QModelIndex].emit(index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row, Maintain())
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.maintains = (self.maintains[:position] + self.maintains[position + rows:])
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
        self.maintains.clear()
        query_sql = 'SELECT id, maintain_date, person, maintain_time FROM maintain WHERE dev_id = :dev_id'
        self.query.prepare(query_sql)
        self.query.bindValue(':dev_id', dev_id)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                maintain = Maintain()
                maintain.id = int(self.query.value(0))
                maintain.maintain_date = float(self.query.value(1))
                maintain.person = float(self.query.value(2))
                maintain.maintain_time = float(self.query.value(3))
                self.maintains.append(maintain)
            self.maintains = sorted(self.maintains, key=lambda x: x.id)
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()
        self.dirty = False

    def delBatchData(self, rows):
        def delOneRow(query, id):
            query_sql = 'DELETE FROM maintain WHERE id = :id'
            query.prepare(query_sql)
            query.bindValue(':id', id)
            if not query.exec_():
                print(query.lastError().text())
            else:
                print('deleted!')

        for row in rows:
            rec_id = self.maintains[row].id
            delOneRow(self.query, rec_id)
        self.maintains = [val for idx, val in enumerate(self.maintains) if idx not in rows]
        self.checkList = [val for idx, val in enumerate(self.checkList) if idx not in rows]

    def updateData(self, maintain):
        query_sql = 'UPDATE maintain SET maintain_date = :maintain_date, person = :person, maintain_time = :maintain_time WHERE id = :id'
        self.query.prepare(query_sql)
        self.query.bindValue(':id', maintain.id)
        self.query.bindValue(':maintain_date', maintain.maintain_date)
        self.query.bindValue(':person', maintain.person)
        self.query.bindValue(':maintain_time', maintain.maintain_time)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            print('updated!')

    def getTotalRecordCount(self, dev_id, begin_date='', end_date=''):
        total_maintain = 0
        query_sql = 'SELECT count(*) FROM maintain WHERE dev_id = :dev_id'
        if begin_date != '' and end_date != '':
            query_sql += " AND maintain_date >= '{0}' AND maintain_date <= '{1}'".format(begin_date, end_date)
        self.query.prepare(query_sql)
        self.query.bindValue(':dev_id', dev_id)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            if self.query.next():
                total_maintain = self.query.value(0)
        return total_maintain

    def getRecordByDevIdAndPages(self, dev_id, limit_index=0, page_count=10, begin_date='', end_date=''):
        self.beginResetModel()
        self.maintains.clear()
        date_query = '' if begin_date == '' or end_date == '' else "AND maintain_date >= '{0}' AND maintain_date <= '{1}'".format(
            begin_date, end_date)
        query_sql = 'SELECT id, maintain_date, person, maintain_time FROM maintain WHERE dev_id = {0} {3} LIMIT {1}, {2}'.format(
            dev_id, limit_index, page_count, date_query)
        self.query.prepare(query_sql)
        if not self.query.exec_():
            print(self.query.lastError().text())
        else:
            while self.query.next():
                maintain = Maintain()
                maintain.id = int(self.query.value(0))
                maintain.maintain_date = str(self.query.value(1))
                maintain.person = str(self.query.value(2))
                maintain.maintain_time = float(self.query.value(3))
                self.maintains.append(maintain)
            self.maintains = sorted(self.maintains, key=lambda x: x.id)
            self.checkList = ['Unchecked'] * self.rowCount()
        self.endResetModel()
        self.dirty = False

    def insertRecord(self, maintain, dev_id):
        insert_sql = 'insert into maintain (maintain_date, person, maintain_time, dev_id) values ' \
                     '(:maintain_date, :person, :maintain_time, :dev_id)'
        self.query.prepare(insert_sql)
        self.query.bindValue(':maintain_date', maintain.maintain_date)
        self.query.bindValue(':person', maintain.person)
        self.query.bindValue(':maintain_time', maintain.maintain_time)
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
