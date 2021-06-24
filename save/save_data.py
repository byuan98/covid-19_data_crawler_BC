# -*- codeing = utf-8 -*-
# @Time : 2020/11/24 11:10
# @Author : ZhangLeifeng
# @File save_data.py
# @Software: PyCharm

# 数据的保存
import datetime
import sqlite3

def saveData(databaseName, dataGlobalTuple, dataChinaTuple, dataChinaCityTuple):
    try:
        globalDataTableCreate(databaseName)
        print("全球疫情当日数据信息表已创建完毕\n")
    except Exception as e:
        print(e)

    try:
        glabalDataTableInput(databaseName, dataGlobalTuple)
    except Exception as e:
        print(e)

    try:
        chinaDataTableCreate(databaseName)
        print("我国疫情数据信息表已创建完毕\n")
    except sqlite3.OperationalError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        chinaDataTableInput(databaseName, dataChinaTuple)

    try:
        chinaCityDataTableCreate(databaseName)
        print("我国主要省市地区当日疫情数据信息表已创建完毕\n")
    except Exception as e:
        print(e)

    try:
        chinaCityDataTableInput(databaseName, dataChinaCityTuple)
    except Exception as e:
        print(e)


# 创建全球疫情当日数据信息表
def globalDataTableCreate(databaseName):
    conn = sqlite3.connect(databaseName)

    today = datetime.date.today().strftime("%Y_%m_%d")  # 日期

    try:
        sqlGlobal = '''
                    create table globalData%s(
                        name text primary key ,
                        nowConfirm number not null ,
                        confirm number not null,
                        heal number not null,
                        dead number not null        
                        )
                        ''' % (today)
        # name 国名
        # nowConfirm 现有确诊
        # confirm 累计确诊
        # heal 累计治愈
        # dead 累计死亡

        cursor = conn.cursor()  # 获取游标
        cursor.execute(sqlGlobal)  # 执行sql语句
        conn.commit()  # 提交数据操作
    except sqlite3.OperationalError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()  # 关闭数据库


# 创建我国疫情数据信息表，该函数需要封装在try中，在执行过一次后一定会出错，所以在调用时应配合将chinaDataTableInput写入finally中
def chinaDataTableCreate(databaseName):
    conn = sqlite3.connect(databaseName)

    try:
        sqlChina = '''
                    create table chinaData(
                        date text primary key ,
                        nowConfirm number not null ,
                        noInfect number not null,
                        importedCase number not null,
                        confirm number not null,
                        heal number not null,
                        dead number not null        
                        )
                        '''
        # date 时间
        # nowConfirm 现有确诊
        # noInfect 无症状感染者
        # importedCase 境外输入
        # confirm 累计确诊
        # heal 累计治愈
        # dead 累计死亡

        cursor = conn.cursor()  # 获取游标
        cursor.execute(sqlChina)
        conn.commit()  # 提交数据操作

    except Exception as e:
        print(e)

    finally:
        conn.close()  # 关闭数据库


# 创建我国主要省市地区当日疫情数据信息表
def chinaCityDataTableCreate(databaseName):
    conn = sqlite3.connect(databaseName)
    today = datetime.date.today().strftime("%Y_%m_%d")  # 日期

    try:
        sqlGlobal = '''
                        create table chinaCityData%s(
                            name text primary key ,
                            nowConfirm number not null ,
                            confirm number not null,
                            heal number not null,
                            dead number not null        
                            )
                            ''' % (today)
        # name 地区名
        # nowConfirm 现有确诊
        # confirm 累计确诊
        # heal 累计治愈
        # dead 累计死亡

        cursor = conn.cursor()  # 获取游标
        cursor.execute(sqlGlobal)  # 执行sql语句
        conn.commit()  # 提交数据操作
    except sqlite3.OperationalError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()  # 关闭数据库


# 将数据写入全球当日疫情数据信息表
def glabalDataTableInput(databaseName, dataGlobalTuple):
    conn = sqlite3.connect(databaseName)

    today = datetime.date.today().strftime("%Y_%m_%d")  # 日期
    cursor = conn.cursor()  # 获取游标

    try:
        count = 0
        for data in dataGlobalTuple:
            sqlGlobalInput = """
                                insert into globalData%s(name,nowConfirm,confirm,heal,dead)
                                values ('%s',%d,%d,%d,%d)     
                                """ % (today, data[0], data[1], data[2], data[3], data[4])

            cursor.execute(sqlGlobalInput)  # 执行sql
            conn.commit()  # 提交数据操作
            count += 1
            print("正在插入globalData%s表的第%d条数据" % (today, count))

        print("\nglobalData%s表数据插入完毕，共插入%d条数据\n" % (today, count))

    except sqlite3.OperationalError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()


# 将数据写入我国疫情数据信息表
def chinaDataTableInput(databaseName, dataChinaTuple):
    conn = sqlite3.connect(databaseName)

    today = datetime.date.today().strftime("%Y_%m_%d")  # 日期

    try:
        count = 1
        sqlChinaInput = """
                    insert into chinaData(date,nowConfirm,noInfect,importedCase,confirm,heal,dead)
                        values ('%s',%d,%d,%d,%d,%d,%d)       
            """ % (today, dataChinaTuple[0], dataChinaTuple[1], dataChinaTuple[2], dataChinaTuple[3], dataChinaTuple[4],
                   dataChinaTuple[5])

        print("正在插入chinaData表的第%d条数据" % (count))

        cursor = conn.cursor()  # 获取游标
        cursor.execute(sqlChinaInput)
        conn.commit()  # 提交数据操作

        print("\nchinaData表数据插入完毕，共插入%d条数据\n" % (count))
    except Exception as e:
        print(e)
    finally:
        conn.close()


# 将数据写入我国主要省市地区当日疫情数据信息表
def chinaCityDataTableInput(databaseName, dataChinaCityTuple):
    conn = sqlite3.connect(databaseName)

    today = datetime.date.today().strftime("%Y_%m_%d")  # 日期
    cursor = conn.cursor()  # 获取游标

    try:
        count = 0
        for data in dataChinaCityTuple:
            sqlchinaCityData = """
                                    insert into chinaCityData%s(name,nowConfirm,confirm,heal,dead)
                                    values ('%s',%d,%d,%d,%d)     
                                    """ % (today, data[0], data[1], data[2], data[3], data[4])

            cursor.execute(sqlchinaCityData)  # 执行sql
            conn.commit()  # 提交数据操作
            count += 1
            print("正在插入chinaCityData%s表的第%d条数据" % (today, count))

        print("\nchinaCityData%s表数据插入完毕，共插入%d条数据\n" % (today, count))
    except Exception as e:
        print(e)
    finally:
        conn.close()


def globalDataTableInput_text(databaseName, dataGlobalTuple):
    conn = sqlite3.connect(databaseName)  # 准备数据库，如果没有该数据库则直接创建
    today = datetime.date.today().strftime("%Y_%m_%d")  # 日期
    cursor = conn.cursor()  # 获取游标
    count = 0  # 计数插入语句的执行条数

    try:
        sqlGlobalTableCreate = '''
                        create table globalData%s(
                            name text primary key ,
                            nowConfirm number not null ,
                            confirm number not null,
                            heal number not null,
                            dead number not null        
                            )
                            ''' % (today)
        # name 国名
        # nowConfirm 现有确诊
        # confirm 累计确诊
        # heal 累计治愈
        # dead 累计死亡
        cursor.execute(sqlGlobalTableCreate)
        conn.commit()  # 提交数据操作

        for data in dataGlobalTuple:
            sqlGlobalTableInput = """
                            insert into globalData%s(name,nowConfirm,confirm,heal,dead)
                            values ('%s',%d,%d,%d,%d)     
                            """ % (today, data[0], data[1], data[2], data[3], data[4])

            cursor.execute(sqlGlobalTableInput)  # 执行sql
            conn.commit()
            count += 1
            print("正在插入globalData%s表的第%d条数据" % (today, count))
        print("\nglobalData%s表数据插入完毕，共插入%d条数据\n" % (today, count))

    except sqlite3.OperationalError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()  # 关闭数据库


def chinaDataTableInput_text(databaseName, dataChinaTuple):
    conn = sqlite3.connect(databaseName)
    today = datetime.date.today().strftime("%Y_%m_%d")  # 日期
    cursor = conn.cursor()  # 获取游标

    try:
        sqlChinaTableCreate = '''
                        create table chinaData(
                            date text primary key ,
                            nowConfirm number not null ,
                            noInfect number not null,
                            importedCase number not null,
                            confirm number not null,
                            heal number not null,
                            dead number not null        
                            )
                            '''
        # date 时间
        # nowConfirm 现有确诊
        # noInfect 无症状感染者
        # importedCase 境外输入
        # confirm 累计确诊
        # heal 累计治愈
        # dead 累计死亡

        cursor.execute(sqlChinaTableCreate)
        conn.commit()  # 提交数据操作

    except Exception as e:
        print(e)
    finally:
        try:
            count = 1
            sqlChinaTableInput = """
                            insert into chinaData(date,nowConfirm,noInfect,importedCase,confirm,heal,dead)
                                values ('%s',%d,%d,%d,%d,%d,%d)       
                    """ % (
                today, dataChinaTuple[0], dataChinaTuple[1], dataChinaTuple[2], dataChinaTuple[3], dataChinaTuple[4],
                dataChinaTuple[5])

            print("正在插入chinaData表的第%d条数据" % (count))
            cursor.execute(sqlChinaTableInput)

            conn.commit()  # 提交数据操作
            print("\nchinaData表数据插入完毕，共插入%d条数据\n" % (count))
        except Exception as e:
            print(e)
        finally:
            conn.close()  # 关闭数据库


def chinaCityDataTableInput_text(databaseName, datachinaTuple):
    pass

# 测试
# if __name__ == '__main__':
#     urlChina = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare"
#     urlGlobal = "https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist"  # 全球 除中国
#     urlChinaCity = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&"
#
#     dataGlobalTuple = analytical_data.analyticalDataGlobal(urlGlobal)
#     dataChinaTuple = analytical_data.analyticalDataChina(urlChina)
#     dataChinaCityTuple = analytical_data.analyticalDataChinaCity(urlChinaCity)
#
#     databaseName = "COVID-19Data_delete.db"
#     saveData(databaseName, dataGlobalTuple, dataChinaTuple, dataChinaCityTuple)
