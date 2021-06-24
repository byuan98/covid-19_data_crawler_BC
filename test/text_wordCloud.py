# -*- codeing = utf-8 -*-
# @Time : 2020/12/19 14:25
# @Author : ZhangLeifeng
# @File text_wordCloud.py
# @Software: PyCharm
import pyecharts.options as opts
from pyecharts.charts import WordCloud

from get_analytical.requests_data import getUrlGet

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://gallery.echartsjs.com/editor.html?c=xS1jMxuOVm

目前无法实现的功能:

1、暂无
"""
url="https://eyesight.news.qq.com/sars/toheros"
data=getUrlGet(url)
data=data["data"]
data=data["allHeros"]
heros=[]
for i in data:
    hero=[]
    hero.append(i["name"]+" "+i["desc"])
    hero.append(0)
    heros.append(hero)

data = heros


(
    WordCloud()
    .add(series_name="热点分析", data_pair=data, word_size_range=[1,6],word_gap = 10,)
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="人民英雄", title_textstyle_opts=opts.TextStyleOpts(font_size=6)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True,
                                      border_width=0

                                      ),
    )
    .render("basic_wordcloud.html")
)

