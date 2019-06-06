import time
import re


def isVaildDate(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def isNumber(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


def gen_date(t_tuple):
    t = time.mktime(t_tuple)
    date_touple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime("%Y-%m-%d", date_touple)  # 将时间元组转成格式化字符串（1976-05-21）
    return date


def compare_date(date1, date2):
    '''确保date2大于date1'''
    b_date = time.mktime(time.strptime(date1, '%Y-%m-%d'))
    e_date = time.mktime(time.strptime(date2, '%Y-%m-%d'))
    return True if int(e_date) - int(b_date) >= 0 else False
