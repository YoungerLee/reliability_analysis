import random
import xlrd, xlwt
item_head = ['时间/h', '温度/℃', '刀头温度/℃', '重复定位精度/μm']
data_num = 1000
def write_excel(filename):
    random.seed(1234)
    excel_file = xlwt.Workbook(encoding='ascii')
    # 获取sheets
    x_axis_sheet = excel_file.add_sheet('X轴')
    y_axis_sheet = excel_file.add_sheet('Y轴')
    z_axis_sheet = excel_file.add_sheet('Z轴')
    font = xlwt.Font()  # Create the Font
    font.name = 'Times New Roman'
    style = xlwt.XFStyle()  # Create the Style
    style.font = font  # Apply the Font to the Style
    # 先写入表头
    for i in range(0, len(item_head)):
        x_axis_sheet.write(0, i, item_head[i])
        y_axis_sheet.write(0, i, item_head[i])
        z_axis_sheet.write(0, i, item_head[i])
    # 写入随机数
    for i in range(0, data_num):
        x_axis_sheet.write(i + 1, 0, i)
        x_axis_sheet.write(i + 1, 1, random.gauss(20, 0.01))
        x_axis_sheet.write(i + 1, 2, random.gauss(25, 0.1) * 0.99)
        x_axis_sheet.write(i + 1, 3, random.gauss(5, 0.1) * 1.01)
    for i in range(0, data_num):
        y_axis_sheet.write(i + 1, 0, i)
        y_axis_sheet.write(i + 1, 1, random.gauss(20, 0.01))
        y_axis_sheet.write(i + 1, 2, random.gauss(25, 0.1) * 0.99)
        y_axis_sheet.write(i + 1, 3, random.gauss(5, 0.1) * 1.01)
    for i in range(0, data_num):
        z_axis_sheet.write(i + 1, 0, i)
        z_axis_sheet.write(i + 1, 1, random.gauss(20, 0.01))
        z_axis_sheet.write(i + 1, 2, random.gauss(25, 0.1) * 0.99)
        z_axis_sheet.write(i + 1, 3, random.gauss(5, 0.1) * 1.01)
    # 保存文档
    excel_file.save(filename)


def read_raw_data(filename):
    '''
    读取原始数据
    :param filename: 文件名
    :return:
    '''
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


def find_fault_time(data_table, temp_thresh, rpa_thresh):
    '''
    统计故障时间间隔
    :param data_table: 数据表
    :param temp_thresh: 温差阈值
    :param rpa_thresh: 精度阈值
    :return:
    '''
    [RUN_TIME, ENV_TEMP, KNI_TEMP, RPA] = [0, 1, 2, 3]
    fault_time = []
    x_table = data_table['x_table']
    y_table = data_table['y_table']
    z_table = data_table['z_table']
    data_num = len(x_table[0])
    for i in range(0, data_num):
        if (x_table[KNI_TEMP][i] - x_table[ENV_TEMP][i] > temp_thresh or x_table[RPA][i] < rpa_thresh) or \
                (y_table[KNI_TEMP][i] - y_table[ENV_TEMP][i] > temp_thresh or y_table[RPA][i] < rpa_thresh) or \
                (z_table[KNI_TEMP][i] - z_table[ENV_TEMP][i] > temp_thresh or z_table[RPA][i] < rpa_thresh):
            fault_time.append(x_table[RUN_TIME][i])
    return fault_time
if __name__ == '__main__':
    data_table = read_raw_data('data.xls')
    print(data_table)
    # fault_time = find_fault_time(data_table, 5, 5)
    # print(len(fault_time))


