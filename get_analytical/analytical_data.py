# -*- codeing = utf-8 -*-
# @Time : 2020/11/24 11:07
# @Author : ZhangLeifeng
# @File analytical_data.py
# @Software: PyCharm

# 数据的解析
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import json
import jsonpath
from get_analytical import requests_data


def jsonConvertDict(url):
    urldata = requests_data.getUrlPost(url)  # 获取页面数据

    print("正在将页面源数据转换为易处理的数据结构\n")

    data = json.loads(urldata)  # 将json类型转为字典

    print("转换完毕\n")

    return data  # 返回处理完毕的数据


def analyticalDataChina(url):
    data = jsonConvertDict(url)
    data = json.loads(data['data'])

    dataChinaList = []

    dataChinaList.append(data['chinaTotal']['nowConfirm'])
    dataChinaList.append(data['chinaTotal']['noInfect'])
    dataChinaList.append(data['chinaTotal']['importedCase'])
    dataChinaList.append(data['chinaTotal']['confirm'])
    dataChinaList.append(data['chinaTotal']['heal'])
    dataChinaList.append(data['chinaTotal']['dead'])

    dataChinaTuple = tuple(dataChinaList)

    return dataChinaTuple


def analyticalDataChinaCity(url):
    data = jsonConvertDict(url)

    data = json.loads(data['data'])['areaTree']  # json.loads(data['data'])先转成字典，然后从areaTree中查看全国数据

    dataChinaCityList = []
    for dataCity in data[0]['children']:  # 0处理字典里套的list
        cityDataTuplePart = (dataCity['name'],
                             dataCity['total']['nowConfirm'],
                             dataCity['total']['confirm'],
                             dataCity['total']['heal'],
                             dataCity['total']['dead']
                             )

        dataChinaCityList.append(cityDataTuplePart)
    dataCityTuple = tuple(dataChinaCityList)
    return dataCityTuple


def analyticalDataGlobal(url):
    data = jsonConvertDict(url)

    print("正在处理获取到的国外疫情数据\n")

    name = jsonpath.jsonpath(data, "$..name")  # 国家名字
    nowConfirm = jsonpath.jsonpath(data, "$..nowConfirm")  # 现有确诊
    confirm = jsonpath.jsonpath(data, "$..confirm")  # 累计确诊
    heal = jsonpath.jsonpath(data, "$..heal")  # 累计治愈
    dead = jsonpath.jsonpath(data, "$..dead")  # 累计死亡

    # print(len(name),len(nowConfirm),len(confirm),len(heal),len(dead)) #测试数据是否在数量上相匹配

    dataGlobalTuple = tuple(zip(name, nowConfirm, confirm, heal, dead))

    print("国外疫情数据处理完毕\n")

    return dataGlobalTuple


def mergingData(urlChina, urlGlobal):
    dataChinaTuple = tuple(['中国']) + analyticalDataChina(urlChina)  # 获取中国疫情数据（元组类型）
    dataGlobalTuple = analyticalDataGlobal(urlGlobal)  # 获取国外疫情数据（元组类型）

    print("正在合并国内外数据\n")

    dataChinaTuple = (
        (dataChinaTuple[0:2] + dataChinaTuple[4:]),
    )  # 由于中国疫情数据会比国外疫情数据更详细，为保证数据数量上的统一性，进行一个切片，最后的逗号是为了将结果转换为一个元组的嵌套，这会方便之后我们合并两个元组

    dataFinal = dataChinaTuple + dataGlobalTuple

    print("数据合并完毕\n")

    return dataFinal
