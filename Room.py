# -*- coding: UTF-8 -*-

import shecdule
import Teacher
import copy


# 考场模型，考场单元
class Room_modle:
    def __init__(self):
        self.ID = ''
        self.vol = -1
        self.needTeacher = -1


class Room_Value:
    room_val = 0

    def __init__(self, val: int):
        self.room_val = val
        self.val_list = [Room_modle()]
        self.val_list.clear()


# 代表考场的空间列表，无时间概念
class Room_List:
    def __init__(self):
        self.list_room = [Room_Value(None)]
        self.num_of_all: int = 0

    def init(self):
        self.list_room.clear()

    def push_pack(self, iRoom: Room_modle):
        for i in self.list_room:
            if iRoom.vol == i.room_val:
                i.val_list.append(iRoom)
                self.num_of_all += 1
                break


# 考场在一时间段的空间列表，时空关系
class Room_TimeSpace:
    def __init__(self, room_cur_list: Room_List, curTime: str, teacher_can_use: Teacher.teacher_list):
        self.room_cur_list = copy.deepcopy(room_cur_list)
        self.curTime = copy.deepcopy(curTime)
        self.teacher_can_use = copy.deepcopy(teacher_can_use)
