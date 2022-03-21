# -*- coding: UTF-8 -*-
# @FILE: DBcon.py
# @Brief: 管理数据库连接
import pymysql


# 创建对已有数据库的连接，返回句柄

def getConnection(iHost, iUser, iPassword, iDbname, iCharset):
    args = dict(
        host=iHost,
        user=iUser,
        passwd=iPassword,
        db=iDbname,
        charset=iCharset
    )
    conn = pymysql.connect(**args)
    return conn


# 新建一个数据库
def createConnection(iHost, iUser, iPassword, iCharset, dbname: str):
    args = dict(
        host=iHost,
        user=iUser,
        passwd=iPassword,
        charset=iCharset
    )
    conn = pymysql.connect(**args)
    cursor = conn.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS " + dbname + " DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
    cursor.execute(sql)
