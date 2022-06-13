# -*- codeing = utf-8 -*-
# @Time : 2020/11/24 11:05
# @Author : ZhangLeifeng
# @File main.py
# @Software: PyCharm

import os
import sys

import constant.path_constant

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(r"C:\Software\Python\venv\Lib\site-packages")
sys.path.append(r"C:\Code\Python\COVID-19_Data\main\COVID-19Data.db")

print(sys.path)

from get_analytical import analytical_data
from save import save_data
from visualization.show_data import dataVisualization

# 主函数，程序入口
if __name__ == '__main__':
    #数据源
    urlChina = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf"
    # 全球(除中国)
    urlGlobal = "https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist"
    urlChinaCity = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf"

    #数据获取与解析
    dataGlobalTuple = analytical_data.mergingData(urlChina,urlGlobal)
    dataChinaTuple = analytical_data.analyticalDataChina(urlChina)
    dataChinaCityTuple = analytical_data.analyticalDataChinaCity(urlChinaCity)

    #准备数据库
    databaseName = constant.path_constant.PathConstant.sqlPath

    #数据库存储
    save_data.saveData(databaseName, dataGlobalTuple, dataChinaTuple, dataChinaCityTuple)

    #进行可视化
    dataVisualization()