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


# def analyticalDataChina(url):
#     data = jsonConvertDict(url)
#
#     print("正在处理获取到的国内疫情数据\n")
#
#     chinaTodayDataDict = {"国家": "中国",
#                           # "日期": str,
#                           "现有确诊": int,
#                           "无症状感染者": int,
#                           "境外输入": int,
#                           "累计确诊": int,
#                           "累计治愈": int,
#                           "累计死亡": int,
#                           }
#     nowConfirmList = jsonpath.jsonpath(data, "$..nowConfirm")  # 现有确诊
#     noInfectList = jsonpath.jsonpath(data, "$..noInfect")  # 无症状感染者
#     importedCaseList = jsonpath.jsonpath(data, "$..importedCase")  # 境外输入
#     confirmList = jsonpath.jsonpath(data, "$..confirm")  # 累计确诊
#     healList = jsonpath.jsonpath(data, "$..heal")  # 累计治愈
#     deadList = jsonpath.jsonpath(data, "$..dead")  # 累计死亡
#
#     '''
#     today = datetime.date.today()  # 日期
#     chinaTodayDataDict["日期"] = today
#     '''
#     nowConfirmToday = nowConfirmList[len(nowConfirmList) - 35]  # 现有确诊，输出nowConfirmList列表会发现，所需数据在倒数第35
#     chinaTodayDataDict["现有确诊"] = nowConfirmToday
#
#     noInfectToday = noInfectList[len(noInfectList) - 1]  # 无症状感染者
#     chinaTodayDataDict["无症状感染者"] = noInfectToday
#
#     importedCaseToday = importedCaseList[len(importedCaseList) - 1]  # 境外输入
#     chinaTodayDataDict["境外输入"] = importedCaseToday
#
#     confirmToday = confirmList[len(confirmList) - 2]  # 累计确诊
#     chinaTodayDataDict["累计确诊"] = confirmToday
#
#     healToday = healList[len(healList) - 35]  # 累计治愈
#     chinaTodayDataDict["累计治愈"] = healToday
#
#     deadToday = deadList[len(deadList) - 35]  # 累计死亡
#     chinaTodayDataDict["累计死亡"] = deadToday
#
#     '''
#     #输出测试
#     print("""
#                  截止至%s
#                  现有确诊：%d
#                  无症状感染者：%d
#                  境外输入：%d
#                  累计确诊：%d
#                  累计治愈：%d
#                  累计死亡：%d
#         """ % (chinaTodayDataDict["日期"],
#                chinaTodayDataDict["现有确诊"],
#                chinaTodayDataDict["无症状感染者"],
#                chinaTodayDataDict["境外输入"],
#                chinaTodayDataDict["累计确诊"],
#                chinaTodayDataDict["累计治愈"],
#                chinaTodayDataDict["累计死亡"]
#                )
#           )
#     '''
#     chinaTodayDataTuple = tuple(chinaTodayDataDict.values())
#
#     print("国内疫情数据处理完毕\n")
#
#     return chinaTodayDataTuple

# def analyticalDataChinaHero():
#     url = "https://eyesight.news.qq.com/sars/toheros"
#     data = get_data_requests.getUrlGet(url)
#     data = data["data"]
#     data = data["allHeros"]
#     heros = []
#     for i in data:
#         hero = []
#         hero.append(i["name"])
#         hero.append(i["desc"])
#         heros.append(hero)
#     print(heros)

def analyticalDataChina(url):
    data = jsonConvertDict(url)
    data = json.loads(data['data'])
    # type(data)=dict
    # print(data.keys())

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

    # type(data)=list,list套了一个dict,dict又套了一个dict

    # print(dataCity['name'])
    # print("现有确诊", dataCity['total']['nowConfirm']) #现有确诊
    # print("累计确诊", dataCity['total']['confirm']) #累计确诊
    # print("累计治愈", dataCity['total']['heal']) #累计治愈
    # print("累计死亡", dataCity['total']['dead']) #累计死亡

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


# 测试
if __name__ == '__main__':
    # urlChina = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare"

    url_global = "https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist"  # 全球 除中国
    # url_china_city = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&"

    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&"
    # analyticalDataChina(url)
    # analyticalDataChinaCity(url)

    # analyticalDataChina(urlChina)
    # analyticalDataGlobal(url_global)
    #
    list = mergingData(url, url_global)
    print(list)
    # jsonConvertDict(url_china_city)

    # analyticalDataChinaCity(url_china_city)

    """
    print("data是一个",type(data),"类型，他的所有主键是：",data.keys())
    print("data[\"data\"]是一个",type(data["data"]),"类型，他的所有主键是：",data["data"].keys())
    print("type(data[\"data\"][\"chinaDayAddList\"])",type(data["data"]["chinaDayAddList"]))
    print("type(data[\"data\"][\"chinaDayAddList\"][0])",type(data["data"]["chinaDayAddList"][0]),"类型，他的所有主键是：",data["data"]["chinaDayAddList"][0].keys())
    """

    """
    print(type(data["data"]["chinaDayAddList"]))
    print(type(data["data"]["chinaDayList"]))
    print(type(data["data"]["cityStatis"]))
    print(type(data["data"]["nowConfirmStatis"]))
    print(type(data["data"]["provinceCompare"]))
    print()
    print(data["data"]["chinaDayList"][len(data["data"]["chinaDayList"])-1]["confirm"])
    """

    # data是一个 <class 'dict'> 类型，他的所有主键是： dict_keys(['ret', 'info', 'data'])
    # data["data"]是一个 <class 'dict'> 类型，他的所有主键是： dict_keys(['chinaDayAddList', 'chinaDayList', 'cityStatis', 'nowConfirmStatis', 'provinceCompare'])
    # type(data["data"]["chinaDayAddList"]) <class 'list'>
    # type(data["data"]["chinaDayAddList"][0]) <class 'dict'> 类型，他的所有主键是： dict_keys(['confirm', 'suspect', 'importedCase', 'healRate', 'dead', 'heal', 'infect', 'deadRate', 'date'])

    # for i in range(0,310):
    #     print(data["data"]["chinaDayAddList"][i])
    #     print("---"*10)
