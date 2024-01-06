# -*- codeing = utf-8 -*-
# 工程启动类
# @Software: PyCharm
# @File main.py
# @Author : ZhangBoyuan
# @Time : 2024/1/6 下午11:10
import bs4
import requests

import constant.url_path

if __name__ == '__main__':
    response = requests.get(url=constant.url_path.get_url_list)
    response.encoding = "utf-8"
    bs = bs4.BeautifulSoup(response.text, "html.parser")

    url_list = []

    for i in bs.find_all("a"):
        if "新型冠状病毒肺炎疫情最新情况" in i.get_text():
            url_list.append("https://www.gov.cn" + i.get("href"))

    print(url_list)

