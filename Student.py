# -*- coding: UTF-8 -*-

# 学生的模型
class student_modle:
    def __init__(self):
        self.name = ''
        self.ID = ''

# 学生在一个原子内的座位信息
class student_seat:
    def __init__(self, seat: int, student_info: student_modle):
        self.seat = seat
        self.student_info = student_info
