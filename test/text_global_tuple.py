# -*- codeing = utf-8 -*-
# @Time : 2020/11/26 19:43
# @Author : ZhangLeifeng
# @File text_global_tuple.py
# @Software: PyCharm

from get_analytical import analytical_data

if __name__ == '__main__':
    url_global = "https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist"  # 全球 除中国

    dataTuple=analytical_data.analyticalDataGlobal(url_global)
    print(dataTuple)

    for i in dataTuple:
        print(i[4])


