# -*- coding: UTF-8 -*-
# @FILE: excel2Mysql.py
# @BRIEF: 实现excel导入数据库

import pymysql.cursors
import DBcon
import xlrd

'''
@brief: 表格导入数据库的入口，传入表的路径即可
@param: 
    database 指定数据库的名称，完成对数据库的连接
    exc_Student 学生表的excel路径
'''


def excel2Sql(database: str, exc_Student: str, exc_Teacher: str, exc_Course: str,
              exc_schedule_early: str, exc_schedule_middle: str, exc_schedule_end: str,
              exc_Room: str, exc_Option: str):
    # 写死登陆信息
    con = DBcon.getConnection('localhost', 'root', , database, 'utf8')
    # 数据库查询游标
    cursor = con.cursor()
    student2Sql(exc_Student, cursor, 'book_student')
    Teacher2Sql(exc_Teacher, cursor, 'book_teacher')
    Room2Sql(exc_Room, cursor, 'book_room')
    option2Sql(exc_Option, cursor, 'book_option')
    Course2Sql(exc_Course, cursor, 'book_course')
    shecdule2Sql(exc_schedule_early, cursor, 'book_schedule_early')
    shecdule2Sql(exc_schedule_middle, cursor, 'book_schedule_middle')
    shecdule2Sql(exc_schedule_end, cursor, 'book_schedule_end')
    # 关闭连接
    con.commit()
    con.close()
    return

'''
 照着这个模式把所有的表写个单独的函数出来就行，参数跟这个形式一样
 课程表的要多加一个统计本门课程人数的功能，通过数据库查询完成，交给库做
'''


def student2Sql(excelName: str, cursor: pymysql.cursors, table: str):
    # 下面代码作用：获取到excel中的字段和数据
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_index(0)
    row_number = sheet.nrows
    column_number = sheet.ncols
    data_list = []
    iRow = 0
    for i in range(1, row_number):
        data_list.append(sheet.row_values(i))
        data_list[iRow][0] = int(data_list[iRow][0])
        data_list[iRow][2] = int(data_list[iRow][2])
        iRow += 1
    # 下面代码作用：根据字段创建表，根据数据执行插入语句
    # 删除语句，若已存在该表，则将该表删除，重新建立
    drop_sql = "drop table if exists {}".format(table)
    cursor.execute(drop_sql)
    # 重新建立指定的表
    # 建立表的元素
    create_sql = "create table {}(".format(table)
    create_sql += "student_ID varchar(50) NOT NULL,"
    create_sql += "student_Name varchar(50),"
    create_sql += "student_Grade varchar(50),"
    create_sql += "student_Sex varchar(50),"
    create_sql += "PRIMARY KEY ( student_ID ) )"
    cursor.execute(create_sql)
    # insert操作
    dataInsert(data_list, cursor, table)


def Teacher2Sql(excelName: str, cursor: pymysql.cursors, table: str):
    # 下面代码作用：获取到excel中的字段和数据
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_index(0)
    row_number = sheet.nrows
    column_number = sheet.ncols
    data_list = []
    iRow = 0
    for i in range(1, row_number):
        data_list.append(sheet.row_values(i))
        data_list[iRow][0] = int(data_list[iRow][0])
        iRow += 1
    # 下面代码作用：根据字段创建表，根据数据执行插入语句
    # 删除语句，若已存在该表，则将该表删除，重新建立
    drop_sql = "drop table if exists {}".format(table)
    print(drop_sql)
    cursor.execute(drop_sql)
    # 重新建立指定的表
    # 建立表的元素
    create_sql = "create table {}(".format(table)
    create_sql += "teacher_ID varchar(50) NOT NULL,"
    create_sql += "teacher_Name varchar(50),"
    create_sql += "teacher_sex varchar(50),"
    create_sql += "Course_Name varchar(50),"
    create_sql += "PRIMARY KEY ( teacher_ID ) )"
    cursor.execute(create_sql)

    # insert操作
    dataInsert(data_list, cursor, table)


def Room2Sql(excelName: str, cursor: pymysql.cursors, table: str):
    # 下面代码作用：获取到excel中的字段和数据
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_index(0)
    row_number = sheet.nrows
    column_number = sheet.ncols
    data_list = []
    iRow = 0
    for i in range(1, row_number):
        data_list.append(sheet.row_values(i))
        data_list[iRow][0] = int(data_list[iRow][0])
        iRow += 1
    # 下面代码作用：根据字段创建表，根据数据执行插入语句
    # 删除语句，若已存在该表，则将该表删除，重新建立
    drop_sql = "drop table if exists {}".format(table)
    print(drop_sql)
    cursor.execute(drop_sql)
    # 重新建立指定的表
    # 建立表的元素
    create_sql = "create table {}(".format(table)
    create_sql += "examination_room_ID varchar(50) NOT NULL,"
    create_sql += "examination_room_volume int,"
    create_sql += "examination_room_teacher int,"
    create_sql += "PRIMARY KEY ( examination_room_ID ) )"
    cursor.execute(create_sql)
    # insert操作
    dataInsert(data_list, cursor, table)


def Course2Sql(excelName: str, cursor: pymysql.cursors, table: str):
    # 下面代码作用：获取到excel中的字段和数据
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_index(0)
    row_number = sheet.nrows
    column_number = sheet.ncols
    data_list = []
    iRow = 0
    for i in range(1, row_number):
        data_list.append(sheet.row_values(i))
        data_list[iRow][0] = int(data_list[iRow][0])
        iRow += 1
    # 下面代码作用：根据字段创建表，根据数据执行插入语句
    # 删除语句，若已存在该表，则将该表删除，重新建立
    drop_sql = "drop table if exists {}".format(table)
    print(drop_sql)
    cursor.execute(drop_sql)
    # 重新建立指定的表
    # 建立表的元素
    create_sql = "create table {}(".format(table)
    create_sql += "Course_ID varchar(50) NOT NULL,"
    create_sql += "Course_Name varchar(50),"
    create_sql += "Course_credit int,"
    create_sql += "Course_exam_num int,"
    create_sql += "num_student int,"
    create_sql += "PRIMARY KEY ( Course_ID ) )"
    cursor.execute(create_sql)
    # insert操作
    data_insert_course(data_list, cursor)


def shecdule2Sql(excelName: str, cursor: pymysql.cursors, table: str):
    # 下面代码作用：获取到excel中的字段和数据
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_index(0)
    row_number = sheet.nrows
    column_number = sheet.ncols
    data_list = []
    for i in range(1, row_number):
        data_list.append(sheet.row_values(i))
    # 下面代码作用：根据字段创建表，根据数据执行插入语句
    # 删除语句，若已存在该表，则将该表删除，重新建立
    drop_sql = "drop table if exists {}".format(table)
    print(drop_sql)
    cursor.execute(drop_sql)
    # 重新建立指定的表
    # 建立表的元素
    create_sql = "create table {}(".format(table)
    create_sql += "time datetime NOT NULL,"
    create_sql += "PRIMARY KEY ( time ) )"
    cursor.execute(create_sql)
    # insert操作
    dataInsert(data_list, cursor, table)


def option2Sql(excelName: str, cursor: pymysql.cursors, table: str):
    # 下面代码作用：获取到excel中的字段和数据
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_index(0)
    row_number = sheet.nrows
    column_number = sheet.ncols
    data_list = []
    iRow = 0
    for i in range(1, row_number):
        data_list.append(sheet.row_values(i))
        data_list[iRow][0] = int(data_list[iRow][0])
        data_list[iRow][3] = int(data_list[iRow][3])
        data_list[iRow][5] = int(data_list[iRow][5])
        iRow += 1
    # 下面代码作用：根据字段创建表，根据数据执行插入语句
    # 删除语句，若已存在该表，则将该表删除，重新建立
    drop_sql = "drop table if exists {}".format(table)
    print(drop_sql)
    cursor.execute(drop_sql)
    # 重新建立指定的表
    # 建立表的元素
    create_sql = "create table {}(".format(table)
    create_sql += "student_ID varchar(50) NOT NULL,"
    create_sql += "student_Name varchar(50),"
    create_sql += "Course_Name varchar(50),"
    create_sql += "Course_ID varchar(50) NOT NULL,"
    create_sql += "teacher_ID varchar(50) NOT NULL,"
    create_sql += "teacher_Name varchar(50),"
    create_sql += "PRIMARY KEY ( Course_ID,teacher_ID,student_ID) )"
    cursor.execute(create_sql)

    # insert操作
    dataInsert(data_list, cursor, table)


def dataInsert(data_list: list, cursor: pymysql.cursors.Cursor, table: str):
    # 遍历数据列表
    for data in data_list:
        new_data = ["'{}'".format(i) for i in data]
        insert_sql = "insert into {} values({})".format(table, ','.join(new_data))
        cursor.execute(insert_sql)


def data_insert_course(data_list: list, cursor: pymysql.cursors.Cursor):
    for data in data_list:
        new_data = ["'{}'".format(i) for i in data]
        new_data[4] = '0'
        insert_sql = "insert into {} values({})".format('book_course', ','.join(new_data))
        cursor.execute(insert_sql)
        count_sql = "select count(*) from book_option where Course_ID="+new_data[0]
        cursor.execute(count_sql)
        results = cursor.fetchone()
        num_student = int(results[0])
        update_sql = "update book_course set num_student={} where Course_ID={}".format(num_student, data[0])
        cursor.execute(update_sql)
