#coding=utf-8
import datetime
import pymysql
import warnings
import pandas as pd
import os
import time
import arrow

warnings.filterwarnings('ignore')

def desktop():
    return os.path.join(os.path.expanduser('~'),'Desktop')

def isLeapYear(years):
    '''
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    # 断言：年份不为整数时，抛出异常。
    assert isinstance(years, int), "请输入整数年，如 2018"

    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        # print(years, "是闰年")
        days_sum = 366
        return days_sum
    else:
        # print(years, '不是闰年')
        days_sum = 365
        return days_sum

def getallYear(years):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)
    # print(all_date_list)
    return all_date_list

def get_str_end_day(year):
    """获取全年月头月尾"""
    list=[]
    for x in range(1, 13):
      dt_start = (datetime.date(year, x, 1))
      if 12 == x:
        dt_end = (datetime.date(year, 12, 31))
      else:
        dt_end = (datetime.date(year, x+1, 1) - datetime.timedelta(days = 1))
      list.append([dt_start,dt_end])
    return list

def time13(date_):#日期转13位时间
    """日期转13位时间戳"""
    date_=str(date_)[:10]
    date_=datetime.date(int(date_[:4]),int(date_[5:7]),int(date_[8:]))
    return int(time.mktime(date_.timetuple()) * 1000)

def get_dateto_13(millis):
    """13位时间戳转日期"""
    return time.strftime('%Y-%m-%d',time.localtime(millis/1000))


def Mysql(db_name):
    pymysql.install_as_MySQLdb()
    host = "localhost"
    port = 3306
    user = 'root'
    password = "sanye"
    connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db_name)
    return connect


def to_mysql(df,db,columns_name,table_name,name):
    connect=Mysql(db)
    new_date = df[columns_name].values[0]
    try:
        df_db = pd.read_sql('select `{}` from {}'.format(columns_name,table_name), con=connect)
        if str(new_date) not in list(df_db[columns_name].values):
            create_engine = ('mysql+mysqldb://root:Mypython@localhost:3306/{}?utf8'.format(db))
            df.to_sql(table_name, create_engine, if_exists='append', index=False)
            print(new_date, '-------------------{}导入成功----------------------'.format(name))
        else:
            print(f'-----------------{name}{new_date}已导入过------------------------')
    except:
        print('{}入失败'.format(name))

