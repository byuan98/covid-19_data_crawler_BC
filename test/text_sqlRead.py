#-*- codeing = utf-8 -*-
#@Time : 2020/12/9 21:26
#@Author : ZhangLeifeng
#@File text_sqlRead.py
#@Software: PyCharm

import sqlite3

conn = sqlite3.connect("D:\Code\Python\COVID-19_Data\main\COVID-19Data.db") #准备数据库

cursor = conn.cursor() #获取游标

sql="""
    select * from chinaData;
"""
cursor.execute(sql)
a=cursor.fetchall()

conn.commit() # 提交数据操作
print(type(a[0]))



