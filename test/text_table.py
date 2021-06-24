# -*- codeing = utf-8 -*-
# @Time : 2020/12/15 19:00
# @Author : ZhangLeifeng
# @File text_table.py
# @Software: PyCharm
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
week_name_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
high_temperature = [11, 11, 15, 13, 12, 13, 10]
low_temperature = [1, -2, 2, 5, 3, 2, 0]


(
    Line(init_opts=opts.InitOpts(width="1600px", height="800px",theme=ThemeType.DARK))
    .add_xaxis(xaxis_data=week_name_list)
    .add_yaxis(
        series_name="最高气温",
        y_axis=high_temperature,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max1", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        ),
    )
    .add_yaxis(
        series_name="最低气温",
        y_axis=low_temperature,
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="average", name="平均值"),
                opts.MarkLineItem(symbol="none", x="90%", y="max1"),
                opts.MarkLineItem(symbol="circle", type_="max1", name="最高点"),
            ]
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="未来一周气温变化", subtitle="纯属虚构"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
    .render("temperature_change_line_chart.html")
)