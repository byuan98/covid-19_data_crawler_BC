# -*- codeing = utf-8 -*-
# @Time : 2020/11/24 11:16
# @Author : ZhangLeifeng
# @File requests_data.py
# @Software: PyCharm

# 原始数据的获取
import requests


def getUrlPost(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"

    }

    try:
        print("正在获取页面源数据\n")
        urlData = requests.post(url, head)

    except:
        print("post请求方式错误，已为您更改为get请求方法\n")
        urlData = requests.get(url, head).json()
    print("页面源数据获取成功\n")

    return urlData.text


def getUrlGet(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"

    }
    urlData = requests.get(url, head).json()

    return urlData

# 测试
# if __name__ == '__main__':
#
#     #url="https://voice.baidu.com/newpneumonia/get?target=trend&isCaseIn=0&stage=publish&callback=jsonp_1607218616427_31597"
#     url="https://eyesight.news.qq.com/sars/toheros"
#     data=getUrlGet(url)
#     data=data["data"]
#     data=data["allHeros"]
#     heros=[]
#     for i in data:
#         hero=[]
#         hero.append(i["name"])
#         hero.append(i["desc"])
#         heros.append(hero)
#     print(heros)

# https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=%E5%8C%97%E4%BA%AC

# data=json.loads(getUrl(urlChina)) #将json类转为字典