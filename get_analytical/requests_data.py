# -*- codeing = utf-8 -*-
# @Time : 2020/11/24 11:16
# @Author : ZhangLeifeng
# @File requests_data.py
# @Software: PyCharm

"""
    原始数据的获取
"""
import requests


def getUrlPost(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"

    }

    print("正在获取页面源数据\n")
    urlData = requests.post(url, head)

    return urlData.text


def getUrlGet(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"

    }
    urlData = requests.get(url, head).json()

    return urlData
