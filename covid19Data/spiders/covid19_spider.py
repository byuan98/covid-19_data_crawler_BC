# -*- coding = utf-8 -*-
# @Software: PyCharm
# @File covid19_spider.py
# @Author : ZhangBoyuan
# @Time : 2025/6/24 10:18

import scrapy
import m49_dict

class Covid19DataSpider(scrapy.Spider):
    name = "covid19Data"

    start_urls = [
        'https://xmart-api-public.who.int/DATA_/RELAY_COVID?$filter=IND_ID%20eq%20%27JVAJ4BACOVID_CASES_CONFIRMED_CUMULATIVE%27%20and%20DIM_TIME_TYPE%20eq%20%27EPI_WEEK%27%20and%20DIM_TIME%20eq%20%27{}%27%20and%20(DIM_GEO_CODE_M49%20eq%20%27001%27%20or%20DIM_GEO_CODE_TYPE%20eq%20%27COUNTRY%27)%20and%20DIM_1_CODE%20eq%20null&$select=DIM_GEO_CODE_M49,DIM_GEO_CODE_TYPE,DIM_TIME,DIM_1_CODE,DIM_2_CODE,DIM_3_CODE,DIM_4_CODE,DIM_5_CODE,DIM_6_CODE,DIM_MEMBER_1_CODE,DIM_MEMBER_2_CODE,DIM_MEMBER_3_CODE,DIM_MEMBER_4_CODE,DIM_MEMBER_5_CODE,DIM_MEMBER_6_CODE,DIM_VALUE_TYPE,VALUE_NUMERIC,VALUE_NUMERIC_LOWER,VALUE_NUMERIC_UPPER,VALUE_LABEL,VALUE_COMMENTS,OBSERVATION_STATUS'
        .format("2025-04-27")
    ]

    def parse(self, response):
        for i in response.json().get('value'):
            if i.get('DIM_GEO_CODE_M49') in m49_dict.m49_to_country.keys():
                print(i.get('DIM_TIME'), i.get('DIM_GEO_CODE_M49'),
                      m49_dict.m49_to_country.get(i.get('DIM_GEO_CODE_M49')),
                      i.get('VALUE_NUMERIC'))



