# -*- codeing = utf-8 -*-
# @Time : 2020/12/5 19:12
# @Author : ZhangLeifeng
# @File text_china_dict.py
# @Software: PyCharm

from get_analytical import analytical_data

if __name__ == '__main__':
    url_china = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare"

    data=analytical_data.analyticalDataChina(url_china)
    print(data)
    list=list(data.values())
    print(list)
