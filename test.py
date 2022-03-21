# -*- coding: UTF-8 -*-
import excel2Mysql
import Arrange

ok = Arrange.enter('gefutest1111'
                   , 'D:/00keshework/excel_test/student.xlsx'
                   , 'D:/00keshework/excel_test/teacher.xlsx'
                   , 'D:/00keshework/excel_test/course.xlsx'
                   , 'D:/00keshework/excel_test/shecdule_early.xlsx'
                   , 'D:/00keshework/excel_test/shecdule_middle.xlsx'
                   , 'D:/00keshework/excel_test/shecdule_end.xlsx'
                   , 'D:/00keshework/excel_test/room.xlsx'
                   , 'D:/00keshework/excel_test/option_list.xlsx'
                   , ""
                   )

if ok < 1:
    if ok == -1:
        print("期末考试所提供的资源不足")
    elif ok == -2:
        print("第二阶段考试提供的资源不足")
    elif ok == -3:
        print("第一阶段考试提供的资源不足")
    else:
        print("未知错误")

elif ok == 1:
    print("考试安排完成")
