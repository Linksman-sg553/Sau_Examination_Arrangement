# -*- coding: UTF-8 -*-

import pymysql.cursors
import DBcon
import xlrd
import xlwt


def work(conn: pymysql.connect, Exam_name: str, dst: str):
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('My Worksheet')
    # 写入excel
    # 生成表头
    worksheet.write(0, 0, label='学号')
    worksheet.write(0, 1, label='学生姓名')
    worksheet.write(0, 2, label='考试阶段')
    worksheet.write(0, 3, label='课程号')
    worksheet.write(0, 4, label='课程名称')
    worksheet.write(0, 5, label='考试时间')
    worksheet.write(0, 6, label='监考老师工号')
    worksheet.write(0, 7, label='监考老师姓名')
    worksheet.write(0, 8, label='考场号')
    worksheet.write(0, 9, label='座位号')
    sql2data(conn, worksheet)
    # 保存
    workbook.save('{}\\{}.xls'.format(dst, Exam_name))


def sql2data(conn: pymysql.connect, worksheet: xlwt.Worksheet):
    sql_find = "select * from book_result"
    cs1 = conn.cursor()
    cs1.execute(sql_find)
    alldata = cs1.fetchall()
    iCursor = 1
    for iData in alldata:
        worksheet.write(iCursor, 0, label=iData[0])
        worksheet.write(iCursor, 1, label=iData[1])
        worksheet.write(iCursor, 2, label=iData[2])
        worksheet.write(iCursor, 3, label=iData[3])
        worksheet.write(iCursor, 4, label=iData[4])
        worksheet.write(iCursor, 5, label=str(iData[5]))
        worksheet.write(iCursor, 6, label=iData[6])
        worksheet.write(iCursor, 7, label=iData[7])
        worksheet.write(iCursor, 8, label=iData[8])
        worksheet.write(iCursor, 9, label=iData[9])
        iCursor += 1


