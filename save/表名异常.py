import os, sqlite3


# connectionobject = sqlite3.connect('1.db', timeout=10, check_same_thread=False)  # 创建连接对象
#
# cursorobject = connectionobject.cursor()  # 创建游标对象
#
# cursorobject.execute("""SELECT * FROM `以哈希分类法处理的文件指向`""")
#
# connectionobject.commit();
#
# tableData = cursorobject.fetchall()
#
# print(tableData)

def formatdatabase(databasepath):
    # print(databasepath+'.db')
    connectionobject = sqlite3.connect(databasepath + '.db', timeout=10, check_same_thread=False)  # 创建连接对象
    cursorobject = connectionobject.cursor()  # 创建游标对象
    connectionobject.execute("create table if not exists 数据库访问log(开启时间 primary key,关闭时间,版本号)")
    connectionobject.execute("create table if not exists 错误log(错误时间 primary key,错误内容,错误时表名,错误时路径)")
    connectionobject.execute(
        "create table if not exists 任务、对应表名、点击位置log(任务开始时间 primary key,开启时间,任务内容,表名,x,y,任务结束时间)")
    connectionobject.execute(
        "create table if not exists 函数调用log(任务开始时间 primary key,开启时间,调用函数名,任务结束时间)")
    connectionobject.execute("create table if not exists 输入log(任务开始时间 primary key,开启时间,输入内容)")
    connectionobject.execute("create table if not exists 弹出窗log(提示时间 primary key,开启时间,弹出内容)")
    connectionobject.execute("create table if not exists 移动log(移动时刻 primary key,原文件位置,现文件位置,异常)")
    connectionobject.execute("create table if not exists 空文件夹清除log(清除时刻 primary key,被清除路径,异常)")
    connectionobject.execute("create table if not exists 窗口鼠标位置log(存在时刻 primary key,x,y,异常)")
    connectionobject.execute("create table if not exists 全局鼠标位置log(存在时刻 primary key,x,y,异常)")
    connectionobject.commit()
    return connectionobject, cursorobject


class DataBaseConnection:
    conn, cursor = formatdatabase('1')


conn, cursor = DataBaseConnection.conn, DataBaseConnection.cursor



for originalpathANDmovedpath in cursor.execute("SELECT 文件夹or名,处理路径 FROM '以哈希分类法处理的文件指向'"):
    conn.commit()
    print(originalpathANDmovedpath)
