from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
import random
import time
import xlrd


def read_raw_data( filename):
    '''
    读取原始数据
    :param filename: 文件名
    :return:
    '''
    item_head = ['时间/h', '温度/℃', '刀头温度/℃', '重复定位精度/μm']
    data_table = dict()  # 保存读取数据
    excel_file = xlrd.open_workbook(filename)
    # 获取sheets, 若不符合所需格式则返回空表
    try:
        x_axis_sheet = excel_file.sheet_by_name('X轴')
        y_axis_sheet = excel_file.sheet_by_name('Y轴')
        z_axis_sheet = excel_file.sheet_by_name('Z轴')
    except xlrd.biffh.XLRDError:
        return data_table
    # 获取表头
    heads = x_axis_sheet.row_values(0)
    if item_head != heads:
        return data_table
    item_num = len(heads)
    # 读取数据
    x_table = [[]] * item_num
    for i in range(0, item_num):
        x_table[i] = x_axis_sheet.col_values(i)[1:]
    y_table = [[]] * item_num
    for i in range(0, item_num):
        y_table[i] = y_axis_sheet.col_values(i)[1:]
    z_table = [[]] * item_num
    for i in range(0, item_num):
        z_table[i] = z_axis_sheet.col_values(i)[1:]
    # 存储
    data_table['x_table'] = x_table
    data_table['y_table'] = y_table
    data_table['z_table'] = z_table
    return data_table

def read_maintain_data(filename):
    '''
    读取维修数据
    :param filename: 文件名
    :return:
    '''
    excel_file = xlrd.open_workbook(filename)
    # 获取sheets
    sheet = excel_file.sheet_by_index(0)
    # 获取表头
    heads = sheet.row_values(0)
    item_num = len(heads)
    # 读取数据
    maintain_table = [[]] * (item_num-1)
    for i in range(0, item_num-1):
        maintain_table[i] = sheet.col_values(i+1)[1:]
    return maintain_table

def read_fault_data(filename):
    '''
    读取故障数据
    :param filename: 文件名
    :return:
    '''
    item_num = 4
    data_table = dict()
    excel_file = xlrd.open_workbook(filename)
    # 获取sheets
    try:
        whole_sheet = excel_file.sheet_by_name('整机')
        subsys_sheet = excel_file.sheet_by_name('子系统')
    except xlrd.biffh.XLRDError:
        return data_table
    # 获取表头
    heads = whole_sheet.row_values(0)
    try:
        patt_col = heads.index('故障模式')
        posi_col = heads.index('故障部位')
        reason_col = heads.index('故障原因')
        root_col = heads.index('故障溯源')
    except ValueError:
        return data_table
    item_idx = [patt_col, posi_col, reason_col, root_col]
    whole_data = [[]] * item_num
    for i in range(0, item_num):
        whole_data[i] = [str(data) for data in whole_sheet.col_values(item_idx[i])[1:]]
    subsys_data = [[]] * item_num
    for i in range(0, item_num):
        subsys_data[i] = [str(data) for data in subsys_sheet.col_values(item_idx[i])[1:]]
    data_table['whole'] = whole_data
    data_table['subsys'] = subsys_data
    return data_table

database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('./db/reliability.db')
database.open()
query = QSqlQuery()
print('create database ok')
sql_str = 'create table device (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, ' \
          'num varchar(50), name varchar(50))'
query.prepare(sql_str)
if not query.exec_():
    print(query.lastError().text())
else:
    print('create a device table')

sql_str = "create table record (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, " \
                      "run_time double, env_temp double, kni_temp double, rpa double, axis variable(5), " \
                      "dev_id int, record_time timestamp NOT NULL DEFAULT(datetime('now','localtime')), " \
                      "foreign key(dev_id) references device(id))"
query.prepare(sql_str)
if not query.exec_():
    print(query.lastError().text())
else:
    print('create a record table')

sql_str = "create table maintain (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, " \
                      "maintain_date date, person varchar(50), maintain_time double, " \
                      "dev_id int, record_time timestamp NOT NULL DEFAULT(datetime('now','localtime')), " \
                      "foreign key(dev_id) references device(id))"
query.prepare(sql_str)
if not query.exec_():
    print(query.lastError().text())
else:
    print('create a maintain table')

sql_str = "create table breakdown (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, " \
                      "pattern varchar(50), position varchar(50), reason varchar(50), root varchar(50), " \
                      "status bit, dev_id int, record_time timestamp NOT NULL DEFAULT(datetime('now','localtime')), " \
                      "foreign key(dev_id) references device(id))"
query.prepare(sql_str)
if not query.exec_():
    print(query.lastError().text())
else:
    print('create a breakdown table')
insert_sql = 'insert into device(num, name) values (:num, :name)'
query.prepare(insert_sql)
query.bindValue(':num', 'abc-123')
query.bindValue(':name', 'dev2')
if not query.exec_():
    print(query.lastError().text())
else:
    print('inserted')

relia_table = read_raw_data('F:\\PyProj\\reliability_analysis\\db\\运行记录表.xlsx')
maintain_table = read_maintain_data('F:\\PyProj\\reliability_analysis\\db\\维修记录表.xlsx')
break_table = read_fault_data('F:\\PyProj\\reliability_analysis\\db\\故障统计表.xlsx')

insert_sql = 'insert into record(run_time, env_temp, kni_temp, rpa, axis, dev_id) values ' \
             '(:run_time, :env_temp, :kni_temp, :rpa, :axis, :dev_id)'
query.prepare(insert_sql)
x_table = relia_table['x_table']
for row in range(0, len(x_table[0])):
    run_time = float(x_table[0][row])
    env_temp = float(x_table[1][row])
    kni_temp = float(x_table[2][row])
    rpa = float(x_table[3][row])
    axis = 'X'
    dev_id = 1
    query.bindValue(':run_time', run_time)
    query.bindValue(':env_temp', env_temp)
    query.bindValue(':kni_temp', kni_temp)
    query.bindValue(':rpa', rpa)
    query.bindValue(':axis', axis)
    query.bindValue(':dev_id', dev_id)
    if not query.exec_():
        print(query.lastError().text())
    else:
        print('inserted')
y_table = relia_table['y_table']
for row in range(0, len(y_table[0])):
    run_time = float(y_table[0][row])
    env_temp = float(y_table[1][row])
    kni_temp = float(y_table[2][row])
    rpa = float(y_table[3][row])
    axis = 'Y'
    dev_id = 1
    query.bindValue(':run_time', run_time)
    query.bindValue(':env_temp', env_temp)
    query.bindValue(':kni_temp', kni_temp)
    query.bindValue(':rpa', rpa)
    query.bindValue(':axis', axis)
    query.bindValue(':dev_id', dev_id)
    if not query.exec_():
        print(query.lastError().text())
    else:
        print('inserted')
z_table = relia_table['z_table']
for row in range(0, len(z_table[0])):
    run_time = float(z_table[0][row])
    env_temp = float(z_table[1][row])
    kni_temp = float(z_table[2][row])
    rpa = float(z_table[3][row])
    axis = 'Z'
    dev_id = 1
    query.bindValue(':run_time', run_time)
    query.bindValue(':env_temp', env_temp)
    query.bindValue(':kni_temp', kni_temp)
    query.bindValue(':rpa', rpa)
    query.bindValue(':axis', axis)
    query.bindValue(':dev_id', dev_id)
    if not query.exec_():
        print(query.lastError().text())
    else:
        print('inserted')

insert_sql = 'insert into maintain (maintain_date, person, maintain_time, dev_id) values ' \
             '(:maintain_date, :person, :maintain_time, :dev_id)'
query.prepare(insert_sql)
for row in range(0, len(maintain_table[0])):
    maintain_date = str(maintain_table[0][row])
    person = str(maintain_table[1][row])
    maintain_time = maintain_table[2][row]
    dev_id = 1
    query.bindValue(':maintain_date', maintain_date)
    query.bindValue(':person', person)
    query.bindValue(':maintain_time', maintain_time)
    query.bindValue(':dev_id', dev_id)
    if not query.exec_():
        print(query.lastError().text())
    else:
        print('inserted')


insert_sql = 'insert into breakdown (pattern, position, reason, root, status, dev_id) values ' \
                             '(:pattern, :position, :reason, :root, :status, :dev_id)'
query.prepare(insert_sql)
whole_table = break_table['whole']
subsys_table = break_table['subsys']
# 整机
for row in range(0, len(whole_table[0])):
    pattern = str(whole_table[0][row])
    position = str(whole_table[1][row])
    reason = str(whole_table[2][row])
    root = str(whole_table[3][row])
    status = 1
    dev_id = 1
    query.bindValue(':pattern', pattern)
    query.bindValue(':position', position)
    query.bindValue(':reason', reason)
    query.bindValue(':root', root)
    query.bindValue(':status', status)
    query.bindValue(':dev_id', dev_id)
    if not query.exec_():
        print(query.lastError().text())
    else:
        print('inserted')

# 子系统
for row in range(0, len(subsys_table[0])):
    pattern = str(subsys_table[0][row])
    position = str(subsys_table[1][row])
    reason = str(subsys_table[2][row])
    root = str(subsys_table[3][row])
    status = 0
    dev_id = 1
    query.bindValue(':pattern', pattern)
    query.bindValue(':position', position)
    query.bindValue(':reason', reason)
    query.bindValue(':root', root)
    query.bindValue(':status', status)
    query.bindValue(':dev_id', dev_id)
    if not query.exec_():
        print(query.lastError().text())
    else:
        print('inserted')

query_sql = 'select id, num, name from device where id = :id'
query.prepare(query_sql)
query.bindValue(':id', 1)
if not query.exec_():
    print(query.lastError())
else:
    while query.next():
        id = query.value(0)
        num = query.value(1)
        name = query.value(2)
        print(id,num,name)

query_sql = 'select * from record where dev_id = :dev_id'
query.prepare(query_sql)
query.bindValue(':dev_id', 1)

if not query.exec_():
    print(query.lastError().text())
else:
    while query.next():
        print(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4), query.value(5), query.value(6), query.value(7))