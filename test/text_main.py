# -*- codeing = utf-8 -*-
# @Time : 2020/12/7 15:53
# @Author : ZhangLeifeng
# @File text_main.py
# @Software: PyCharm

from get_analytical import analytical_data
from save import save_data

if __name__ == '__main__':
    urlChina = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&"
    urlGlobal = "https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist"  # 全球 除中国
    urlChinaCity = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&"

    #dataGlobalTuple = analytical_data.analyticalDataGlobal(urlGlobal)
    dataGlobalTuple=analytical_data.mergingData(urlChina,urlGlobal)
    dataChinaTuple = analytical_data.analyticalDataChina(urlChina)
    dataChinaCityTuple = analytical_data.analyticalDataChinaCity(urlChinaCity)

    databaseName = "COVID-19Data_text.db"

    save_data.saveData(databaseName, dataGlobalTuple, dataChinaTuple, dataChinaCityTuple)
