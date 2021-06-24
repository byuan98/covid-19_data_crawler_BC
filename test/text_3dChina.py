# -*- codeing = utf-8 -*-
# @Time : 2020/12/18 20:11
# @Author : ZhangLeifeng
# @File text_3dChina.py
# @Software: PyCharm

import datetime
import sqlite3
from pyecharts import options as opts
from pyecharts.charts import Map3D, Timeline
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode

conn = sqlite3.connect("D:\Code\Python\COVID-19_Data\main\COVID-19Data.db")  # 准备数据库
today = datetime.date.today().strftime("%Y_%m_%d")
cursor = conn.cursor()  # 获取游标
sql = """
                select * from chinaCityData%s;
            """ % (today)
cursor.execute(sql)
conn.commit()  # 提交数据操作
dataList = cursor.fetchall()


def maxData(listData):
    listNumber = []
    for i in listData:
        listNumber.append(i[1])
    listNumber.sort()
    maxNumber = listNumber[-2]
    return maxNumber


dataNowConfirm, dataConfirm, dataHeal, dataDead = [], [], [], []
for i in dataList:
    dataNowConfirm.append(i[0:2])
    dataConfirm.append(i[0:1] + i[2:3])
    dataHeal.append(i[0:1] + i[3:4])
    dataDead.append(i[0:1] + i[4:5])

# example_data = [
#         ["黑龙江", [127.9688, 45.368, 100]],
#         ("内蒙古", [110.3467, 41.4899, 300]),
#         ("吉林", [125.8154, 44.2584, 300]),
#         ("辽宁", [123.1238, 42.1216, 300]),
#         ("河北", [114.4995, 38.1006, 300]),
#         ("天津", [117.4219, 39.4189, 300]),
#         ("山西", [112.3352, 37.9413, 300]),
#         ("陕西", [109.1162, 34.2004, 300]),
#         ("甘肃", [103.5901, 36.3043, 300]),
#         ("宁夏", [106.3586, 38.1775, 300]),
#         ("青海", [101.4038, 36.8207, 300]),
#         ("新疆", [87.9236, 43.5883, 300]),
#         ("西藏", [91.11, 29.97, 300]),
#         ("四川", [103.9526, 30.7617, 300]),
#         ("重庆", [108.384366, 30.439702, 300]),
#         ("山东", [117.1582, 36.8701, 300]),
#         ("河南", [113.4668, 34.6234, 300]),
#         ("江苏", [118.8062, 31.9208, 300]),
#         ("安徽", [117.29, 32.0581, 300]),
#         ("湖北", [114.3896, 30.6628, 300]),
#         ("浙江", [119.5313, 29.8773, 300]),
#         ("福建", [119.4543, 25.9222, 300]),
#         ("江西", [116.0046, 28.6633, 300]),
#         ("湖南", [113.0823, 28.2568, 300]),
#         ("贵州", [106.6992, 26.7682, 300]),
#         ("广西", [108.479, 23.1152, 300]),
#         ("海南", [110.3893, 19.8516, 300]),
#         ("上海", [121.4648, 31.2891, 1300]),
#     ]
# for i in range(0,len(example_data)):
#     example_data[i]=list(example_data[i])
#     example_data[i][1][2]=dataNowConfirm[i][1]
#     example_data[i]=tuple(example_data[i])
#
# print(example_data)
example_data = {
    "黑龙江": [127.9688, 45.368],
    "内蒙古": [110.3467, 41.4899],
    "吉林": [125.8154, 44.2584],
    "辽宁": [123.1238, 42.1216],
    "河北": [114.4995, 38.1006],
    "天津": [117.4219, 39.4189],
    "山西": [112.3352, 37.9413],
    "陕西": [109.1162, 34.2004],
    "甘肃": [103.5901, 36.3043],
    "宁夏": [106.3586, 38.1775],
    "青海": [101.4038, 36.8207],
    "新疆": [87.9236, 43.5883],
    "西藏": [91.11, 29.97],
    "四川": [103.9526, 30.7617],
    "重庆": [108.384366, 30.439702],
    "山东": [117.1582, 36.8701],
    "河南": [113.4668, 34.6234],
    "江苏": [118.8062, 31.9208],
    "安徽": [117.29, 32.0581],
    "湖北": [114.3896, 30.6628],
    "浙江": [119.5313, 29.8773],
    "福建": [119.4543, 25.9222],
    "江西": [116.0046, 28.6633],
    "湖南": [113.0823, 28.2568],
    "贵州": [106.6992, 26.7682],
    "广西": [108.479, 23.1152],
    "海南": [110.3893, 19.8516],
    "上海": [121.4648, 31.2891],
    "香港": [114.1, 22.2],
    "台湾": [121.08, 24],
    "广东": [113.23, 23.16],
    "云南": [102.73, 25.04],
    "北京": [116.39, 39.91],
    "澳门": [113.54, 22.20]
}
example = []

for i in dataNowConfirm:
    example.append(list(i[0].split()))

for i in example:
    list1 = example_data[i[0]]
    i.append(list1)

for i, j in zip(example, dataNowConfirm):
    if j[1]==0:
        continue
    i[1].append(j[1])

c = (
    Map3D()
        .add_schema(itemstyle_opts=opts.ItemStyleOpts(
        color="rgb(5,101,123)",
        opacity=1,
        border_width=0.8,
        border_color="rgb(62,215,213)",
    ),
        map3d_label=opts.Map3DLabelOpts(
            is_show=False,
            formatter=JsCode("function(data){return data.name + " " + data.value[2];}"),
        ),
        emphasis_label_opts=opts.LabelOpts(
            is_show=False,
            color="#fff",
            font_size=10,
            background_color="rgba(0,23,11,0)",
        ),
        light_opts=opts.Map3DLightOpts(
            main_color="#fff",
            main_intensity=1.2,
            main_shadow_quality="high",
            is_main_shadow=True,
            main_beta=10,
            ambient_intensity=0.3,
        ),
    )
        .add(
        series_name="world",
        data_pair=example,
        type_=ChartType.BAR3D,
        bar_size=1,
        shading="lambert",
        label_opts=opts.LabelOpts(
            is_show=False,
            formatter=JsCode("function(data){return data.name + '现有确诊：' + data.value[2];}"),
        ),
    )
        .set_global_opts(title_opts=opts.TitleOpts(title="Map3D-Bar3D"))
        .render("11.html")
)
