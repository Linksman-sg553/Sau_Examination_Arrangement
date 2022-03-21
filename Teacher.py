# -*- coding: UTF-8 -*-

class teacher_modle:
    def __init__(self):
        self.name = ''
        self.ID = ''
        self.course = ''


class teacher_list:

    def __init__(self):
        self.list_teacher = [teacher_modle()]

    def init(self):
        self.list_teacher.clear()

    def push_back(self, data: teacher_modle):
        self.list_teacher.append(data)


class teacher_space:
    def __init__(self, cur_list: teacher_list, cur_time: str):
        self.cur_list = cur_list
        self.cur_time = cur_time
