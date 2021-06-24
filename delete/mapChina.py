# -*- codeing = utf-8 -*-
# @Time : 2020/12/15 21:05
# @Author : ZhangLeifeng
# @File test_mapGlobal.py
# @Software: PyCharm
import sqlite3
import datetime
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline
from pyecharts.globals import ThemeType


def maxData(listData):
    listNumber = []
    for i in listData:
        listNumber.append(i[1])
    listNumber.sort()
    maxNumber = listNumber[-2]
    return maxNumber


def mapChina():
    conn = sqlite3.connect("D:\Code\Python\COVID-19_Data\main\COVID-19Data.db")  # 准备数据库
    today = datetime.date.today().strftime("%Y_%m_%d")
    cursor = conn.cursor()  # 获取游标
    sql = """
                select * from chinaCityData%s;
            """ % (today)
    cursor.execute(sql)
    conn.commit()  # 提交数据操作
    dataList = cursor.fetchall()

    dataNowConfirm, dataConfirm, dataHeal, dataDead = [], [], [], []
    for i in dataList:
        dataNowConfirm.append(i[0:2])
        dataConfirm.append(i[0:1] + i[2:3])
        dataHeal.append(i[0:1] + i[3:4])
        dataDead.append(i[0:1] + i[4:5])

    listTitle = ["现有确诊", "累计确诊", "累计治愈", "累计死亡"]
    tl = Timeline()

    for i in listTitle:
        if i == "现有确诊":
            l = dataNowConfirm
            max1 = maxData(l)
        elif i == "累计确诊":
            l = dataConfirm
            max1 = maxData(l)
        elif i == "累计治愈":
            l = dataHeal
            max1 = maxData(l)
        else:
            l = dataDead
            max1 = maxData(l)
        map = (

            Map(init_opts=opts.InitOpts(theme=ThemeType.WALDEN
                                        )
                )
                .add(i,
                     data_pair=l,
                     maptype="china",
                     is_map_symbol_show=True,
                     )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="中国主要省市疫情数据(%s)" % (i)
                                          ),
                visualmap_opts=opts.VisualMapOpts(max_=max1,
                                                  min_=1
                                                  )
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False
                                                           )
                                 )
        )
        tl.add(map, "{}".format(i))
    print(type(tl))

if __name__ == '__main__':
    mapChina()