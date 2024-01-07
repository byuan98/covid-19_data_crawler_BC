# -*- coding = utf-8 -*-
# 工程启动类
# @Software: PyCharm
# @File main.py
# @Author : ZhangBoyuan
# @Time : 2024/1/6 下午11:10
import sqlite3

import bs4
import requests

from constant.url_path import UrlPath


def get_covid19_content_url_list():
    result = []

    response = requests.get(url=UrlPath.INDEX_URL)
    response.encoding = "utf-8"
    bs = bs4.BeautifulSoup(response.text, "html.parser")

    for i in bs.find_all("a"):
        if "新型冠状病毒肺炎疫情最新情况" in i.get_text():
            result.append("https://www.gov.cn" + i.get("href"))

    return result


if __name__ == '__main__':
    covid19_content_url_list = get_covid19_content_url_list()

    conn = sqlite3.connect("../static/covid-19.db")
    cur = conn.cursor()

    for covid19_content_url in covid19_content_url_list:
        response = requests.get(url=covid19_content_url)
        response.encoding = "utf-8"
        bs = bs4.BeautifulSoup(response.text, "html.parser")
        url_content = bs.find(id="UCAP-CONTENT").find_all("p")

        title = bs.title.string
        content = ""

        for i in url_content:
            content = content + i.get_text()

        sql = """insert into data_source values ('%s', '%s', '%s');""" % (covid19_content_url, title, content)

        cur.execute(sql)
        conn.commit()

    cur.close()
    conn.close()
