# -*- codeing = utf-8 -*-
# @Time : 2020/12/17 22:19
# @Author : ZhangLeifeng
# @File show_data.py
# @Software: PyCharm

import datetime
import sqlite3

from pyecharts import options as opts
from pyecharts.charts import Map, Page, Map3D, Timeline, Line, WordCloud, MapGlobe
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType

from constant import path_constant
from get_analytical.requests_data import getUrlGet

databasePath = path_constant.PathConstant.sqlPath


# 数据库表数据查询
def consultTable(tableName):
    conn = sqlite3.connect(databasePath)
    cursor = conn.cursor()
    sql = """
        select * from %s;
                """ % (tableName)
    cursor.execute(sql)
    conn.commit()  # 提交数据操作
    tableData = cursor.fetchall()
    conn.close()
    return tableData


# 寻找第二大的值
def maxData(listData):
    listNumber = []
    for i in listData:
        listNumber.append(i[1])
    listNumber.sort()
    maxNumber = listNumber[-2]
    return maxNumber


# 中国地图
def mapChina():
    today = datetime.date.today().strftime("%Y_%m_%d")
    tableName = "chinaCityData%s" % (today)
    dataList = consultTable(tableName)

    dataNowConfirm, dataConfirm, dataHeal, dataDead = [], [], [], []
    for i in dataList:
        dataNowConfirm.append(i[0:2])
        dataConfirm.append(i[0:1] + i[2:3])
        dataHeal.append(i[0:1] + i[3:4])
        dataDead.append(i[0:1] + i[4:5])

    listTitle = ["现有确诊", "累计确诊", "累计治愈", "累计死亡"]
    tl = Timeline(init_opts=opts.InitOpts(width="100%")).add_schema(orient="orient", is_auto_play=True)

    for i in listTitle:
        if i == "现有确诊":
            l = dataNowConfirm
            max1 = maxData(l)
        elif i == "累计确诊":
            l = dataConfirm
            max1 = maxData(l)
        elif i == "累计治愈":
            l = dataHeal
            max1 = maxData(l)
        else:
            l = dataDead
            max1 = maxData(l)
        map = (Map(init_opts=opts.InitOpts(theme=ThemeType.WALDEN, width="100%", bg_color="#FAF9DE"))
               .add(series_name=i, data_pair=l, maptype="china", is_map_symbol_show=True, )
               .set_global_opts(
            title_opts=opts.TitleOpts(title="中国主要省市疫情数据(%s)" % (i), pos_left="center", pos_top="10px"),
            visualmap_opts=opts.VisualMapOpts(max_=max1, is_show=True, item_height=400, item_width=25,
                                              orient="vertical", pos_left=25, pos_bottom=5,
                                              range_text=["Max", "Min"], split_number=60000, ),
            legend_opts=opts.LegendOpts(is_show=True, pos_left="center", pos_top=32, ), )
               .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                                effect_opts=opts.EffectOpts(is_show=True, brush_type="fill")))
        tl.add(map, "{}".format(i))
    return tl


# 中国地图（3d）
def mapChina3d():
    today = datetime.date.today().strftime("%Y_%m_%d")
    tableName = "chinaCityData%s" % (today)
    dataList = consultTable(tableName)

    dataNowConfirm = []
    for i in dataList:
        dataNowConfirm.append(i[0:2])

    example_data = {
        "黑龙江": [127.9688, 45.368],
        "内蒙古": [110.3467, 41.4899],
        "吉林": [125.8154, 44.2584],
        "辽宁": [123.1238, 42.1216],
        "河北": [114.4995, 38.1006],
        "天津": [117.4219, 39.4189],
        "山西": [112.3352, 37.9413],
        "陕西": [109.1162, 34.2004],
        "甘肃": [103.5901, 36.3043],
        "宁夏": [106.3586, 38.1775],
        "青海": [101.4038, 36.8207],
        "新疆": [87.9236, 43.5883],
        "西藏": [91.11, 29.97],
        "四川": [103.9526, 30.7617],
        "重庆": [108.384366, 30.439702],
        "山东": [117.1582, 36.8701],
        "河南": [113.4668, 34.6234],
        "江苏": [118.8062, 31.9208],
        "安徽": [117.29, 32.0581],
        "湖北": [114.3896, 30.6628],
        "浙江": [119.5313, 29.8773],
        "福建": [119.4543, 25.9222],
        "江西": [116.0046, 28.6633],
        "湖南": [113.0823, 28.2568],
        "贵州": [106.6992, 26.7682],
        "广西": [108.479, 23.1152],
        "海南": [110.3893, 19.8516],
        "上海": [121.4648, 31.2891],
        "香港": [114.1, 22.2],
        "台湾": [121.08, 24],
        "广东": [113.23, 23.16],
        "云南": [102.73, 25.04],
        "北京": [116.39, 39.91],
        "澳门": [113.54, 22.20]
    }
    example = []

    for i in dataNowConfirm:
        example.append(list(i[0].split()))

    for i in example:
        list1 = example_data[i[0]]
        i.append(list1)

    for i, j in zip(example, dataNowConfirm):
        if j[1] == 0:
            continue
        i[1].append(j[1])

    c = (
        Map3D(init_opts=opts.InitOpts(width="100%", height="600px", bg_color="#FAF9DE"))
        .add_schema(itemstyle_opts=opts.ItemStyleOpts(
            color="rgb(5,101,123)", opacity=1, border_width=0.8, border_color="rgb(62,215,213)",
        ),
            # 显示地面
            is_show_ground=True,
            # 将地面设置为白色
            ground_color="#FAF9DE",
            map3d_label=opts.Map3DLabelOpts(is_show=False, formatter=JsCode(
                "function(data){return data.name + " " + data.value[2];}"), ),
            emphasis_label_opts=opts.LabelOpts(
                is_show=False, color="#fff",
                font_size=10,
                background_color="rgba(0,23,11,0)",
            ),
            light_opts=opts.Map3DLightOpts(
                main_color="#fff",
                main_intensity=1.2,
                main_shadow_quality="ultra",
                is_main_shadow=True,
                main_beta=10,
                ambient_intensity=0.3,
            ),
            post_effect_opts=opts.Map3DPostEffectOpts(
                # 开启光晕特效
                is_bloom_enable=True,
                # 设置光晕强度
                bloom_intensity=0.1,
            ),
        )
        .add(
            series_name="现有确诊",
            data_pair=example,
            type_=ChartType.BAR3D,
            bar_size=1,
            shading="lambert",
            label_opts=opts.LabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + '现存确诊：' + data.value[2];}"),
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="我国现存确诊省份", pos_left="center", ),
                         legend_opts=opts.LegendOpts(is_show=True, pos_top=32)))
    return c


# 全球地图
def mapGlobal():
    today = datetime.date.today().strftime("%Y_%m_%d")
    tableName = "globalData%s" % (today)
    dataList = consultTable(tableName)
    mapGlobal3D()

    dataNowConfirm, dataConfirm, dataHeal, dataDead = [], [], [], []

    for i in dataList:
        dataNowConfirm.append(i[0:2])
        dataConfirm.append(i[0:1] + i[2:3])
        dataHeal.append(i[0:1] + i[3:4])
        dataDead.append(i[0:1] + i[4:5])

    listTitle = ["现有确诊", "累计确诊", "累计治愈", "累计死亡"]
    tl = Timeline(init_opts=opts.InitOpts(width="100%")).add_schema(orient="orient", is_auto_play=True)
    nameMap = {
        'Singapore Rep.': '新加坡',
        'Dominican Rep.': '多米尼加',
        'Palestine': '巴勒斯坦',
        'Bahamas': '巴哈马',
        'Timor-Leste': '东帝汶',
        'Afghanistan': '阿富汗',
        'Guinea-Bissau': '几内亚比绍',
        "C?te d'Ivoire": '科特迪瓦',
        'Siachen Glacier': '锡亚琴冰川',
        "Br. Indian Ocean Ter.": '英属印度洋领土',
        'Angola': '安哥拉',
        'Albania': '阿尔巴尼亚',
        'United Arab Emirates': '阿联酋',
        'Argentina': '阿根廷',
        'Armenia': '亚美尼亚',
        'French Southern and Antarctic Lands': '法属南半球和南极领地',
        'Australia': '澳大利亚',
        'Austria': '奥地利',
        'Azerbaijan': '阿塞拜疆',
        'Burundi': '布隆迪',
        'Belgium': '比利时',
        'Benin': '贝宁',
        'Burkina Faso': '布基纳法索',
        'Bangladesh': '孟加拉',
        'Bulgaria': '保加利亚',
        'The Bahamas': '巴哈马',
        'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
        'Belarus': '白俄罗斯',
        'Belize': '伯利兹',
        'Bermuda': '百慕大',
        'Bolivia': '玻利维亚',
        'Brazil': '巴西',
        'Brunei': '文莱',
        'Bhutan': '不丹',
        'Botswana': '博茨瓦纳',
        'Central African Rep.': '中非共和国',
        'Canada': '加拿大',
        'Switzerland': '瑞士',
        'Chile': '智利',
        'China': '中国',
        'Ivory Coast': '象牙海岸',
        'Cameroon': '喀麦隆',
        'Dem. Rep. Congo': '刚果（布）',
        'Congo': '刚果（金）',
        'Colombia': '哥伦比亚',
        'Costa Rica': '哥斯达黎加',
        'Cuba': '古巴',
        'N. Cyprus': '北塞浦路斯',
        'Cyprus': '塞浦路斯',
        'Czech Rep.': '捷克',
        'Germany': '德国',
        'Djibouti': '吉布提',
        'Denmark': '丹麦',
        'Algeria': '阿尔及利亚',
        'Ecuador': '厄瓜多尔',
        'Egypt': '埃及',
        'Eritrea': '厄立特里亚',
        'Spain': '西班牙',
        'Estonia': '爱沙尼亚',
        'Ethiopia': '埃塞俄比亚',
        'Finland': '芬兰',
        'Fiji': '斐济',
        'Falkland Islands': '福克兰群岛',
        'France': '法国',
        'Gabon': '加蓬',
        'United Kingdom': '英国',
        'Georgia': '格鲁吉亚',
        'Ghana': '加纳',
        'Guinea': '几内亚',
        'Gambia': '冈比亚',
        'Guinea Bissau': '几内亚比绍',
        'Eq. Guinea': '赤道几内亚',
        'Greece': '希腊',
        'Greenland': '格陵兰',
        'Guatemala': '危地马拉',
        'French Guiana': '法属圭亚那',
        'Guyana': '圭亚那',
        'Honduras': '洪都拉斯',
        'Croatia': '克罗地亚',
        'Haiti': '海地',
        'Hungary': '匈牙利',
        'Indonesia': '印度尼西亚',
        'India': '印度',
        'Ireland': '爱尔兰',
        'Iran': '伊朗',
        'Iraq': '伊拉克',
        'Iceland': '冰岛',
        'Israel': '以色列',
        'Italy': '意大利',
        'Jamaica': '牙买加',
        'Jordan': '约旦',
        'Japan': '日本',
        'Japan': '日本本土',
        'Kazakhstan': '哈萨克斯坦',
        'Kenya': '肯尼亚',
        'Kyrgyzstan': '吉尔吉斯斯坦',
        'Cambodia': '柬埔寨',
        'Korea': '韩国',
        'Kosovo': '科索沃',
        'Kuwait': '科威特',
        'Lao PDR': '老挝',
        'Lebanon': '黎巴嫩',
        'Liberia': '利比里亚',
        'Libya': '利比亚',
        'Sri Lanka': '斯里兰卡',
        'Lesotho': '莱索托',
        'Lithuania': '立陶宛',
        'Luxembourg': '卢森堡',
        'Latvia': '拉脱维亚',
        'Morocco': '摩洛哥',
        'Moldova': '摩尔多瓦',
        'Madagascar': '马达加斯加',
        'Mexico': '墨西哥',
        'Macedonia': '马其顿',
        'Mali': '马里',
        'Myanmar': '缅甸',
        'Montenegro': '黑山',
        'Mongolia': '蒙古',
        'Mozambique': '莫桑比克',
        'Mauritania': '毛里塔尼亚',
        'Malawi': '马拉维',
        'Malaysia': '马来西亚',
        'Namibia': '纳米比亚',
        'New Caledonia': '新喀里多尼亚',
        'Niger': '尼日尔',
        'Nigeria': '尼日利亚',
        'Nicaragua': '尼加拉瓜',
        'Netherlands': '荷兰',
        'Norway': '挪威',
        'Nepal': '尼泊尔',
        'New Zealand': '新西兰',
        'Oman': '阿曼',
        'Pakistan': '巴基斯坦',
        'Panama': '巴拿马',
        'Peru': '秘鲁',
        'Philippines': '菲律宾',
        'Papua New Guinea': '巴布亚新几内亚',
        'Poland': '波兰',
        'Puerto Rico': '波多黎各',
        'Dem. Rep. Korea': '朝鲜',
        'Portugal': '葡萄牙',
        'Paraguay': '巴拉圭',
        'Qatar': '卡塔尔',
        'Romania': '罗马尼亚',
        'Russia': '俄罗斯',
        'Rwanda': '卢旺达',
        'W. Sahara': '西撒哈拉',
        'Saudi Arabia': '沙特阿拉伯',
        'Sudan': '苏丹',
        'S. Sudan': '南苏丹',
        'Senegal': '塞内加尔',
        'Solomon Is.': '所罗门群岛',
        'Sierra Leone': '塞拉利昂',
        'El Salvador': '萨尔瓦多',
        'Somaliland': '索马里兰',
        'Somalia': '索马里',
        'Serbia': '塞尔维亚',
        'Suriname': '苏里南',
        'Slovakia': '斯洛伐克',
        'Slovenia': '斯洛文尼亚',
        'Sweden': '瑞典',
        'Swaziland': '斯威士兰',
        'Syria': '叙利亚',
        'Chad': '乍得',
        'Togo': '多哥',
        'Thailand': '泰国',
        'Tajikistan': '塔吉克斯坦',
        'Turkmenistan': '土库曼斯坦',
        'East Timor': '东帝汶',
        'Trinidad and Tobago': '特里尼达和多巴哥',
        'Tunisia': '突尼斯',
        'Turkey': '土耳其',
        'Tanzania': '坦桑尼亚',
        'Uganda': '乌干达',
        'Ukraine': '乌克兰',
        'Uruguay': '乌拉圭',
        'United States': '美国',
        'Uzbekistan': '乌兹别克斯坦',
        'Venezuela': '委内瑞拉',
        'Vietnam': '越南',
        'Vanuatu': '瓦努阿图',
        'West Bank': '西岸',
        'Yemen': '也门',
        'South Africa': '南非',
        'Zambia': '赞比亚',
        'Zimbabwe': '津巴布韦'
    }

    for i in listTitle:
        if i == "现有确诊":
            l = dataNowConfirm
            max1 = maxData(l)
        elif i == "累计确诊":
            l = dataConfirm
            max1 = maxData(l)
        elif i == "累计治愈":
            l = dataHeal
            max1 = maxData(l)
        else:
            l = dataDead
            max1 = maxData(l)
        map = (
            Map(init_opts=opts.InitOpts(theme=ThemeType.WALDEN, width="100%", height="600px", bg_color="#FAF9DE"))
            .add(i, data_pair=l, maptype="world", name_map=nameMap, is_map_symbol_show=True, )
            .set_global_opts(title_opts=opts.TitleOpts(title="COVID-19全球疫情数据",
                                                       pos_left="center",
                                                       title_link=r"D:\Code\Final\COVID-19_Data\main\mapGlobal.html",
                                                       title_textstyle_opts=opts.TextStyleOpts(font_size=25,)),
                             visualmap_opts=opts.VisualMapOpts(max_=max1,
                                                               is_show=True,
                                                               item_height=400,
                                                               item_width=25,
                                                               orient="vertical",
                                                               pos_left=25,
                                                               pos_bottom=5,
                                                               range_text=["Max", "Min"],
                                                               ),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_left="center",
                                                         pos_top=32,
                                                         ),
                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False,

                                                       ),

                             )
        )
        tl.add(map, "{}".format(i))
    return tl


# 全球地图（3d）
def mapGlobal3D():
    conn = sqlite3.connect(databasePath)
    today = datetime.date.today().strftime("%Y_%m_%d")
    cursor = conn.cursor()

    sql = """
            select * from globalData%s;
        """ % (today)

    cursor.execute(sql)
    conn.commit()
    dataList = cursor.fetchall()
    conn.close()

    example_data = []
    for i in dataList:
        example_data.append(i[0:2])
    nameMap = {
        'Singapore Rep.': '新加坡',
        'Dominican Rep.': '多米尼加',
        'Palestine': '巴勒斯坦',
        'Bahamas': '巴哈马',
        'Timor-Leste': '东帝汶',
        'Afghanistan': '阿富汗',
        'Guinea-Bissau': '几内亚比绍',
        "C?te d'Ivoire": '科特迪瓦',
        'Siachen Glacier': '锡亚琴冰川',
        "Br. Indian Ocean Ter.": '英属印度洋领土',
        'Angola': '安哥拉',
        'Albania': '阿尔巴尼亚',
        'United Arab Emirates': '阿联酋',
        'Argentina': '阿根廷',
        'Armenia': '亚美尼亚',
        'French Southern and Antarctic Lands': '法属南半球和南极领地',
        'Australia': '澳大利亚',
        'Austria': '奥地利',
        'Azerbaijan': '阿塞拜疆',
        'Burundi': '布隆迪',
        'Belgium': '比利时',
        'Benin': '贝宁',
        'Burkina Faso': '布基纳法索',
        'Bangladesh': '孟加拉',
        'Bulgaria': '保加利亚',
        'The Bahamas': '巴哈马',
        'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
        'Belarus': '白俄罗斯',
        'Belize': '伯利兹',
        'Bermuda': '百慕大',
        'Bolivia': '玻利维亚',
        'Brazil': '巴西',
        'Brunei': '文莱',
        'Bhutan': '不丹',
        'Botswana': '博茨瓦纳',
        'Central African Rep.': '中非共和国',
        'Canada': '加拿大',
        'Switzerland': '瑞士',
        'Chile': '智利',
        'China': '中国',
        'Ivory Coast': '象牙海岸',
        'Cameroon': '喀麦隆',
        'Dem. Rep. Congo': '刚果（布）',
        'Congo': '刚果（金）',
        'Colombia': '哥伦比亚',
        'Costa Rica': '哥斯达黎加',
        'Cuba': '古巴',
        'N. Cyprus': '北塞浦路斯',
        'Cyprus': '塞浦路斯',
        'Czech Rep.': '捷克',
        'Germany': '德国',
        'Djibouti': '吉布提',
        'Denmark': '丹麦',
        'Algeria': '阿尔及利亚',
        'Ecuador': '厄瓜多尔',
        'Egypt': '埃及',
        'Eritrea': '厄立特里亚',
        'Spain': '西班牙',
        'Estonia': '爱沙尼亚',
        'Ethiopia': '埃塞俄比亚',
        'Finland': '芬兰',
        'Fiji': '斐济',
        'Falkland Islands': '福克兰群岛',
        'France': '法国',
        'Gabon': '加蓬',
        'United Kingdom': '英国',
        'Georgia': '格鲁吉亚',
        'Ghana': '加纳',
        'Guinea': '几内亚',
        'Gambia': '冈比亚',
        'Guinea Bissau': '几内亚比绍',
        'Eq. Guinea': '赤道几内亚',
        'Greece': '希腊',
        'Greenland': '格陵兰',
        'Guatemala': '危地马拉',
        'French Guiana': '法属圭亚那',
        'Guyana': '圭亚那',
        'Honduras': '洪都拉斯',
        'Croatia': '克罗地亚',
        'Haiti': '海地',
        'Hungary': '匈牙利',
        'Indonesia': '印度尼西亚',
        'India': '印度',
        'Ireland': '爱尔兰',
        'Iran': '伊朗',
        'Iraq': '伊拉克',
        'Iceland': '冰岛',
        'Israel': '以色列',
        'Italy': '意大利',
        'Jamaica': '牙买加',
        'Jordan': '约旦',
        'Japan': '日本',
        'Japan': '日本本土',
        'Kazakhstan': '哈萨克斯坦',
        'Kenya': '肯尼亚',
        'Kyrgyzstan': '吉尔吉斯斯坦',
        'Cambodia': '柬埔寨',
        'Korea': '韩国',
        'Kosovo': '科索沃',
        'Kuwait': '科威特',
        'Lao PDR': '老挝',
        'Lebanon': '黎巴嫩',
        'Liberia': '利比里亚',
        'Libya': '利比亚',
        'Sri Lanka': '斯里兰卡',
        'Lesotho': '莱索托',
        'Lithuania': '立陶宛',
        'Luxembourg': '卢森堡',
        'Latvia': '拉脱维亚',
        'Morocco': '摩洛哥',
        'Moldova': '摩尔多瓦',
        'Madagascar': '马达加斯加',
        'Mexico': '墨西哥',
        'Macedonia': '马其顿',
        'Mali': '马里',
        'Myanmar': '缅甸',
        'Montenegro': '黑山',
        'Mongolia': '蒙古',
        'Mozambique': '莫桑比克',
        'Mauritania': '毛里塔尼亚',
        'Malawi': '马拉维',
        'Malaysia': '马来西亚',
        'Namibia': '纳米比亚',
        'New Caledonia': '新喀里多尼亚',
        'Niger': '尼日尔',
        'Nigeria': '尼日利亚',
        'Nicaragua': '尼加拉瓜',
        'Netherlands': '荷兰',
        'Norway': '挪威',
        'Nepal': '尼泊尔',
        'New Zealand': '新西兰',
        'Oman': '阿曼',
        'Pakistan': '巴基斯坦',
        'Panama': '巴拿马',
        'Peru': '秘鲁',
        'Philippines': '菲律宾',
        'Papua New Guinea': '巴布亚新几内亚',
        'Poland': '波兰',
        'Puerto Rico': '波多黎各',
        'Dem. Rep. Korea': '朝鲜',
        'Portugal': '葡萄牙',
        'Paraguay': '巴拉圭',
        'Qatar': '卡塔尔',
        'Romania': '罗马尼亚',
        'Russia': '俄罗斯',
        'Rwanda': '卢旺达',
        'W. Sahara': '西撒哈拉',
        'Saudi Arabia': '沙特阿拉伯',
        'Sudan': '苏丹',
        'S. Sudan': '南苏丹',
        'Senegal': '塞内加尔',
        'Solomon Is.': '所罗门群岛',
        'Sierra Leone': '塞拉利昂',
        'El Salvador': '萨尔瓦多',
        'Somaliland': '索马里兰',
        'Somalia': '索马里',
        'Serbia': '塞尔维亚',
        'Suriname': '苏里南',
        'Slovakia': '斯洛伐克',
        'Slovenia': '斯洛文尼亚',
        'Sweden': '瑞典',
        'Swaziland': '斯威士兰',
        'Syria': '叙利亚',
        'Chad': '乍得',
        'Togo': '多哥',
        'Thailand': '泰国',
        'Tajikistan': '塔吉克斯坦',
        'Turkmenistan': '土库曼斯坦',
        'East Timor': '东帝汶',
        'Trinidad and Tobago': '特里尼达和多巴哥',
        'Tunisia': '突尼斯',
        'Turkey': '土耳其',
        'Tanzania': '坦桑尼亚',
        'Uganda': '乌干达',
        'Ukraine': '乌克兰',
        'Uruguay': '乌拉圭',
        'United States': '美国',
        'Uzbekistan': '乌兹别克斯坦',
        'Venezuela': '委内瑞拉',
        'Vietnam': '越南',
        'Vanuatu': '瓦努阿图',
        'West Bank': '西岸',
        'Yemen': '也门',
        'South Africa': '南非',
        'Zambia': '赞比亚',
        'Zimbabwe': '津巴布韦'
    }
    low, high = 6599950, 0
    mapGlobe = (MapGlobe(init_opts=opts.InitOpts(bg_color="#228fbd", width="1500px"))
                .add(name_map=nameMap,
                     maptype="world",
                     series_name="国家",
                     data_pair=example_data,
                     label_opts=opts.LabelOpts(is_show=False),
                     )

                .set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=True,
                                                               trigger="axis",
                                                               is_always_show_content=True,
                                                               ),
                                 visualmap_opts=opts.VisualMapOpts(min_=low,
                                                                   max_=high,
                                                                   range_color=["lightskyblue", "yellow", "red"]
                                                                   ),
                                 )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True
                                                           )
                                 )  # 显示国家名字
                .render("mapGlobal.html")
                )


# 中国疫情数据折线图
def lineChina():
    x_data = []
    y_data = ["nowConfirm", "noInfect", "importedCase", "confirm", "heal", "dead"]

    for i in range(-4, 1):
        today = (datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y_%m_%d")
        x_data.append(today)

    def sqlChaxun(listName):

        tableData = []
        for j in x_data:
            conn = sqlite3.connect(databasePath)
            cursor = conn.cursor()
            sql = """
            select %s from chinaData
            where date='%s'

                """ % (listName, j)
            cursor.execute(sql)
            conn.commit()
            tableData.append(cursor.fetchall())
            conn.close()

        return tableData

    dataNowConfirm = sqlChaxun(y_data[0])  # 现有确诊
    dataNoInfect = sqlChaxun(y_data[1])  # 无症状感染者
    dataImportedCase = sqlChaxun(y_data[2])  # 累计境外输入
    dataConfirm = sqlChaxun(y_data[3])  # 累计确诊
    dataHeal = sqlChaxun(y_data[4])  # 累计治愈
    dataDead = sqlChaxun(y_data[5])  # 累计死亡

    c = (
        Line(init_opts=opts.InitOpts(width="100%", height="500px", bg_color="#FAF9DE"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="现有确诊",
            stack="总量",
            y_axis=dataNowConfirm,
            symbol="triangle",
            symbol_size=10,
            linestyle_opts=opts.Lines3DEffectOpts(
                is_show=True,
                period=1,
                trail_width=10,
                trail_length=1,
            ),

            label_opts=opts.LabelOpts(is_show=True),
        )
        .add_yaxis(
            series_name="无症状感染者",
            stack="总量",
            y_axis=dataNoInfect,
            symbol="Chad",
            symbol_size=10,
            label_opts=opts.LabelOpts(is_show=True),
            linestyle_opts=opts.Lines3DEffectOpts(
                is_show=True,
                period=1,
                trail_width=10,
                trail_length=1,
            ),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkAreaItem(type_="add_yaxis")])

        )
        .add_yaxis(
            series_name="累计境外输入",
            stack="总量",
            y_axis=dataImportedCase,
            symbol="pin",
            symbol_size=10,
            linestyle_opts=opts.Lines3DEffectOpts(
                is_show=True,
                period=1,
                trail_width=10,
                trail_length=1,
            ),
            label_opts=opts.LabelOpts(is_show=True),
        )
        .add_yaxis(
            series_name="累计确诊",
            stack="总量",
            y_axis=dataConfirm,
            symbol="roundRect",
            symbol_size=10,
            linestyle_opts=opts.Lines3DEffectOpts(
                is_show=True,
                period=1,
                trail_width=10,
                trail_length=1,
            ),
            label_opts=opts.LabelOpts(is_show=True),
        )
        .add_yaxis(
            series_name="累计治愈",
            stack="总量",
            y_axis=dataHeal,
            symbol="arrow",
            symbol_size=10,
            linestyle_opts=opts.Lines3DEffectOpts(
                is_show=True,
                period=1,
                trail_width=10,
                trail_length=1,
            ),
            label_opts=opts.LabelOpts(is_show=True),
        )
        .add_yaxis(
            series_name="累计死亡",
            stack="总量",
            y_axis=dataDead,
            symbol="diamond",
            symbol_size=10,
            linestyle_opts=opts.Lines3DEffectOpts(
                is_show=True,
                period=1,
                trail_width=10,
                trail_length=1,
            ),
            label_opts=opts.LabelOpts(is_show=True),
        )

        .set_global_opts(
            title_opts=opts.TitleOpts(title="中国疫情数据信息",
                                      pos_left="center"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(type_="value",
                                     axistick_opts=opts.AxisTickOpts(is_show=True),
                                     splitline_opts=opts.SplitLineOpts(is_show=True),
                                     ),
            xaxis_opts=opts.AxisOpts(type_="category",
                                     boundary_gap=False),
            legend_opts=opts.LegendOpts(pos_top=32),

            toolbox_opts=opts.ToolboxOpts(
                is_show=True,  # 是否显示工具栏组件
                orient="vertical",
                pos_left="left",

            )

        )

    )
    return c


# 人民英雄词云
def wordCloudHero():
    url = "https://eyesight.news.qq.com/sars/toheros"
    data = getUrlGet(url)
    data = data["data"]
    data = data["allHeros"]
    heros = []
    for i in data:
        hero = []
        hero.append(i["name"] + ":" + i["desc"])
        hero.append(0)
        heros.append(hero)

    data = heros

    c = (
        WordCloud(init_opts=opts.InitOpts(width="100%", height="500px", bg_color="#FAF9DE"))
        .add(series_name="人民英雄",
             data_pair=data,
             word_size_range=[1, 10],
             word_gap=0,
             shape="circle",
             is_draw_out_of_bound=True,
             rotate_step=1
             )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title_textstyle_opts=opts.TextStyleOpts(font_size=20),
                pos_left="center",
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True,
                                          border_width=0
                                          ),
        )
    )
    return c


def dataVisualization():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        mapGlobal(),
        mapChina(),
        mapChina3d(),
        lineChina(),
        # wordCloudHero()
    )
    page.render("final.html")


if __name__ == '__main__':
    # page = Page(layout=Page.DraggablePageLayout)  # 自定义布局
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        mapGlobal(),
        mapChina(),
        mapChina3d(),
        lineChina(),
        wordCloudHero()
    )
    page.render("initial.html")
