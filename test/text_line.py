# -*- codeing = utf-8 -*-
# @Time : 2020/12/19 12:28
# @Author : ZhangLeifeng
# @File text_line.py
# @Software: PyCharm
import sqlite3
import pyecharts.options as opts
from pyecharts.charts import Line
import datetime

x_data = []
y_data = ["nowConfirm", "noInfect", "importedCase", "confirm", "heal", "dead"]
dataNowConfirm, dataNoInfect, dataImportedCase, dataConfirm, dataHeal, dataDead = [], [], [], [], [], []

for i in range(-4, 1):
    today = (datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y_%m_%d")
    x_data.append(today)


def sqlChaxun(listName):

    tableData = []
    for j in x_data:

        conn = sqlite3.connect("D:\Code\Python\COVID-19_Data\main\COVID-19Data.db")  # 准备数据库
        cursor = conn.cursor()  # 获取游标
        sql = """
        select %s from chinaData
        where date='%s'
    
            """ % (listName, j)
        cursor.execute(sql)
        conn.commit()  # 提交数据操作
        tableData.append(cursor.fetchall())
        conn.close()

    return tableData


dataNowConfirm = sqlChaxun(y_data[0])
dataNoInfect = sqlChaxun(y_data[1])
dataImportedCase = sqlChaxun(y_data[2])
dataConfirm = sqlChaxun(y_data[3])
dataHeal = sqlChaxun(y_data[4])
dataDead = sqlChaxun(y_data[5])

c=(
    Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
        series_name="现有确诊",
        stack="总量",
        y_axis=dataNowConfirm,
        label_opts=opts.LabelOpts(is_show=True),
    )
        .add_yaxis(
        series_name="无症状感染者",
        stack="总量",
        y_axis=dataNoInfect,
        label_opts=opts.LabelOpts(is_show=True),
    )
        .add_yaxis(
        series_name="累计境外输入",
        stack="总量",
        y_axis=dataImportedCase,
        label_opts=opts.LabelOpts(is_show=True),
    )
        .add_yaxis(
        series_name="累计确诊",
        stack="总量",
        y_axis=dataConfirm,
        label_opts=opts.LabelOpts(is_show=True),
    )
        .add_yaxis(
        series_name="累计治愈",
        stack="总量",
        y_axis=dataHeal,
        label_opts=opts.LabelOpts(is_show=True),
    )
        .add_yaxis(
        series_name="累计死亡",
        stack="总量",
        y_axis=dataDead,
        label_opts=opts.LabelOpts(is_show=True),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="折线图堆叠"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )

)
print(type(c))
