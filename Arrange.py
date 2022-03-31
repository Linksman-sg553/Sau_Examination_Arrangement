# -*- coding: UTF-8 -*-
import excel2Mysql
import Room
import DBcon
import Teacher
import Course
import Student
import pymysql
import copy
import sql2excel

'''
1.导入excel done
2.读取数据库获取Rooms生成列表 done 
3.读取数据库获取Teacher生成列表 done
4.读取数据库获取Schedule生成列表 done
5.根据Schedule生成TimeSpace done
6.遍历课程表，生成Course对象 done
7.为Course读取学生列表   done
8.依据阶段分开原则，处理阶段考 done
10.依据TimeSpace去处理分配问题 done
'''


raw_list_Room = Room.Room_List()
raw_list_teacher = Teacher.teacher_list()
schedule_list_early = []
schedule_list_middle = []
schedule_list_end = []
timeSpace_list_early = [Room.Room_TimeSpace(None, None, None)]
timeSpace_list_middle = [Room.Room_TimeSpace(None, None, None)]
timeSpace_list_end = [Room.Room_TimeSpace(None, None, None)]
course_list = [Course.Course_modle(None, None, None)]


def enter(database: str, exc_Student: str, exc_Teacher: str, exc_Course: str,
          exc_schedule_early: str, exc_schedule_middle: str, exc_schedule_end: str,
          exc_Room: str, exc_Option: str, dst: str):
    # 上传excel至数据库
    DBcon.createConnection('localhost', 'root', 'gefu1128', 'utf8', database)
    excel2Mysql.excel2Sql(database, exc_Student, exc_Teacher, exc_Course,
                          exc_schedule_early, exc_schedule_middle, exc_schedule_end,
                          exc_Room, exc_Option)
    # 创建数据库句柄
    conn = DBcon.getConnection('localhost', 'root', 'gefu1128', database, 'utf8')

    # 创建列表
    create_Room_list(conn)
    create_Teacher_list(conn)
    create_Course(conn)
    create_schedule_list(conn)
    create_timeSpace(conn)

    # 分配原子
    for iCourse in course_list:
        # 上传的资源不够分配当前考试
        # 不同阶段使用不同的时空列表
        if iCourse.exam_stage == 3:
            if len(timeSpace_list_early) == 0:
                return -3
            arrange_Course_early(iCourse)
        elif iCourse.exam_stage == 2:
            if len(timeSpace_list_middle) == 0:
                return -2
            arrange_Course_middle(iCourse)
        elif iCourse.exam_stage == 1:
            if len(timeSpace_list_end) == 0:
                return -1
            arrange_Course_end(iCourse)
        # 让课程的原子分配学生

        iCourse.allocate_student()

    data2sql(conn)
    sql2excel.work(conn, database, dst)
    conn.close()
    return 1


def arrange_Course_early(iCourse: Course.Course_modle):
    idx = 0
    while idx < len(timeSpace_list_early):
        # 测试
        # 检查当前列表可用状态
        if timeSpace_list_early[idx].room_cur_list.num_of_all == 0:
            # 不可用，剔除
            timeSpace_list_early.remove(timeSpace_list_early[idx])
            # 保证下面执行的语句使用的列表是可用的
            continue
        # 列表可用，分配操作
        isOver_1 = iCourse.allocate_atom(timeSpace_list_early[idx])
        # 监考教师人手不足
        if isOver_1 == -1:
            # 将本时间列表去掉,顺位至下一个时间列表，继续为本课程分配
            timeSpace_list_early.remove(timeSpace_list_early[idx])
            continue
        # 发现人没分完教室也剩余了
        elif isOver_1 > 0 and timeSpace_list_early[idx].room_cur_list.num_of_all > 0:
            isOver_2 = iCourse.allocate_atom_reverse(timeSpace_list_early[idx])
        # 正好分完
        elif isOver_1 == 0:
            return True
    # 传入参数未经正确分配，因列表不够用，退出，返回不可用状态
    return False


def arrange_Course_middle(iCourse: Course.Course_modle):
    idx = 0
    while idx < len(timeSpace_list_middle):
        # 检查当前列表可用状态
        if timeSpace_list_middle[idx].room_cur_list.num_of_all == 0:
            # 不可用，剔除
            timeSpace_list_middle.remove(timeSpace_list_middle[idx])
            # 保证下面执行的语句使用的列表是可用的
            continue
        # 列表可用，分配操作
        isOver_1 = iCourse.allocate_atom(timeSpace_list_middle[idx])
        # 监考教师人手不足
        if isOver_1 == -1:
            # 将本时间列表去掉,顺位至下一个时间列表，继续为本课程分配
            timeSpace_list_middle.remove(timeSpace_list_middle[idx])
            continue
        # 发现人没分完教室也剩余了
        elif isOver_1 > 0 and timeSpace_list_middle[idx].room_cur_list.num_of_all > 0:
            isOver_2 = iCourse.allocate_atom_reverse(timeSpace_list_middle[idx])
        # 正好分完
        elif isOver_1 == 0:
            return True
    # 传入参数未经正确分配，因列表不够用，退出，返回不可用状态
    return False


def arrange_Course_end(iCourse: Course.Course_modle):
    idx = 0
    while idx < len(timeSpace_list_end):
        # 检查当前列表可用状态
        if timeSpace_list_end[idx].room_cur_list.num_of_all == 0:
            # 不可用，剔除
            timeSpace_list_end.remove(timeSpace_list_end[idx])
            # 保证下面执行的语句使用的列表是可用的
            continue
        # 列表可用，分配操作
        isOver_1 = iCourse.allocate_atom(timeSpace_list_end[idx])
        # 监考教师人手不足
        if isOver_1 == -1:
            # 将本时间列表去掉,顺位至下一个时间列表，继续为本课程分配
            timeSpace_list_end.remove(timeSpace_list_end[idx])
            continue
        # 发现人没分完教室也剩余了
        elif isOver_1 > 0 and timeSpace_list_end[idx].room_cur_list.num_of_all > 0:
            isOver_2 = iCourse.allocate_atom_reverse(timeSpace_list_end[idx])
        # 正好分完
        elif isOver_1 == 0:
            return True
    # 传入参数未经正确分配，因列表不够用，退出，返回不可用状态
    return False


def create_Room_list(conn: pymysql.connect):
    raw_list_Room.init()
    cs1 = conn.cursor()

    # 生成货币原则的指向队列
    sql_distinct = 'select distinct examination_room_volume from book_room;'
    cs1.execute(sql_distinct)
    allData_vol = cs1.fetchall()
    data_val = []
    for i in allData_vol:
        data_val.append(int(i[0]))
    data_val.sort(reverse=True)

    for i in data_val:
        iRoomVal = Room.Room_Value(i)
        raw_list_Room.list_room.append(iRoomVal)

    # 插入元素
    sql1 = 'SELECT examination_room_ID, examination_room_volume, examination_room_teacher from book_room'
    cs1.execute(sql1)
    alldata = cs1.fetchall()
    for iData in alldata:
        raw_data = Room.Room_modle()
        raw_data.ID = str(iData[0])
        raw_data.vol = int(iData[1])
        raw_data.needTeacher = int(iData[2])
        raw_list_Room.push_pack(raw_data)

    cs1.close()


def create_Teacher_list(conn: pymysql.connect):
    raw_list_teacher.init()
    cs1 = conn.cursor()
    sql1 = 'SELECT teacher_ID, teacher_Name, Course_Name from book_teacher'
    cs1.execute(sql1)
    alldata = cs1.fetchall()
    for iData in alldata:
        raw_data = Teacher.teacher_modle()
        raw_data.ID = str(iData[0])
        raw_data.name = str(iData[1])
        raw_data.course = str(iData[2])
        raw_list_teacher.push_back(raw_data)
    cs1.close()


def create_schedule_list(conn: pymysql.connect):
    cs1 = conn.cursor()
    sql1 = 'SELECT time from book_schedule_early'
    sql2 = 'SELECT time from book_schedule_middle'
    sql3 = 'SELECT time from book_schedule_end'

    cs1.execute(sql1)
    alldata = cs1.fetchall()
    for iData in alldata:
        raw_data = str(iData[0])
        schedule_list_early.append(raw_data)

    cs1.execute(sql2)
    alldata = cs1.fetchall()
    for iData in alldata:
        raw_data = str(iData[0])
        schedule_list_middle.append(raw_data)

    cs1.execute(sql3)
    alldata = cs1.fetchall()
    for iData in alldata:
        raw_data = str(iData[0])
        schedule_list_end.append(raw_data)
    cs1.close()


def create_timeSpace(conn: pymysql.connect):
    timeSpace_list_early.clear()
    timeSpace_list_middle.clear()
    timeSpace_list_end.clear()
    for iTime in schedule_list_early:
        iSpace = Room.Room_TimeSpace(raw_list_Room, iTime, raw_list_teacher)
        timeSpace_list_early.append(iSpace)

    for iTime in schedule_list_middle:
        iSpace = Room.Room_TimeSpace(raw_list_Room, iTime, raw_list_teacher)
        timeSpace_list_middle.append(iSpace)

    for iTime in schedule_list_end:
        iSpace = Room.Room_TimeSpace(raw_list_Room, iTime, raw_list_teacher)
        timeSpace_list_end.append(iSpace)


def create_Course(conn: pymysql.connect):
    # 初始化清空课程列表
    course_list.clear()
    cs1 = conn.cursor()
    # 查询语句
    sql1 = 'SELECT Course_Name, Course_ID, num_student, Course_exam_num from book_course'
    cs1.execute(sql1)
    alldata = cs1.fetchall()
    # 根据查询列表创建课程
    for iData in alldata:
        # 判断考试阶段正确性
        if iData[3] > 3 or iData[3] <= 0:
            return False
        # 判断考试分几阶段
        course_num: int = iData[3]
        # 创建学生选修列表
        list_optionStudent = [Student.student_modle()]
        list_optionStudent.clear()
        list_optionStudent = get_student(iData[1], conn)
        while not course_num == 1:
            iCourse_side = Course.Course_modle(iData[0], iData[1],iData[2])
            iCourse_side.exam_stage = course_num
            iCourse_side.list_student = copy.deepcopy(list_optionStudent)
            course_num -= 1
            course_list.append(iCourse_side)
        iCourse = Course.Course_modle(iData[0], iData[1], iData[2])
        iCourse.exam_stage = course_num
        iCourse.list_student = copy.deepcopy(list_optionStudent)
        course_list.append(iCourse)
    cs1.close()


def read_studentList(conn: pymysql.connect):
    cs1 = conn.cursor()
    for iCourse in course_list:
        sql_findStudent = 'select student_ID, student_Name from book_option where Course_ID = ' + str(iCourse.ID)
        cs1.execute(sql_findStudent)
        alldata = cs1.fetchall()
        for iData in alldata:
            iStudent = Student.student_modle()
            iStudent.ID = iData[0]
            iStudent.name = iData[1]
            iCourse.list_student.append(iStudent)
    cs1.close()


def data2sql(conn: pymysql.connect):
    cs1 = conn.cursor()
    drop_sql = "drop table if exists {}".format('book_result')
    print(drop_sql)
    cs1.execute(drop_sql)
    sql_create = "create table {}(".format('book_result')
    sql_create += "student_ID varchar(50) NOT NULL,"
    sql_create += "student_Name varchar(50),"
    sql_create += "Course_stage varchar(50),"
    sql_create += "Course_ID varchar(50) NOT NULL,"
    sql_create += "Course_Name varchar(50),"
    sql_create += "time datetime NOT NULL,"
    sql_create += "teacher_ID varchar(1000) NOT NULL,"
    sql_create += "teacher_Name varchar(1000),"
    sql_create += "examination_room_ID varchar(50) NOT NULL,"
    sql_create += "seat varchar(50) NOT NULL,"
    sql_create += "PRIMARY KEY ( student_ID,  Course_ID, examination_room_ID, Course_stage, time, seat) )"
    cs1.execute(sql_create)
    for iCourse in course_list:
        val_CourseID = "'{}'".format(iCourse.ID)
        val_CourseName = "'{}'".format(iCourse.Name)
        val_CourseStage = ""
        if iCourse.exam_stage == 1:
            val_CourseStage = "'{}'".format("期末")
        elif iCourse.exam_stage == 2:
            val_CourseStage = "'{}'".format("第二次")
        elif iCourse.exam_stage == 3:
            val_CourseStage = "'{}'".format("第一次")
        for iAtom in iCourse.list_atom:
            val_time = "'{}'".format(iAtom.time)
            val_Room = "'{}'".format(iAtom.Room.ID)
            val_TeacherName = "'"
            val_TeacherID = "'"
            for iTeacher in iAtom.list_teacher:
                val_TeacherName += iTeacher.name
                val_TeacherName += ','
                val_TeacherID += iTeacher.ID
                val_TeacherID += ','

            val_TeacherName += "'"
            val_TeacherID += "'"
            for iSeat in iAtom.list_seat:
                val_seat = "'{}'".format(str(iSeat.seat))
                val_StudentID = "'{}'".format(iSeat.student_info.ID)
                val_StudentName = "'{}'".format(iSeat.student_info.name)
                new_data = [val_StudentID, val_StudentName, val_CourseStage, val_CourseID, val_CourseName, val_time, val_TeacherID,
                            val_TeacherName, val_Room, val_seat]
                insert_sql = "insert into book_result values({})".format(
                    ','.join(new_data)
                )
                print(insert_sql)
                cs1.execute(insert_sql)
    conn.commit()
    cs1.close()


def get_student(Course_ID: str, conn: pymysql.connect):
    find_sql = "select student_Name, student_ID from book_option where Course_ID=" + Course_ID
    cs1 = conn.cursor()
    cs1.execute(find_sql)
    alldata = cs1.fetchall()
    list_ssss = [Student.student_modle()]
    list_ssss.clear()
    for iData in alldata:
        iStudent = Student.student_modle()
        iStudent.ID = iData[1]
        iStudent.name = iData[0]
        list_ssss.append(iStudent)
    cs1.close()
    return list_ssss
