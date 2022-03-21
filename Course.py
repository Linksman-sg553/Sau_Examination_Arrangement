# -*- coding: UTF-8 -*-
import random
import Student
import Teacher
import Room
import Exam_atom
import conflict_ditect
import math


class Course_modle:

    def __init__(self, Name: str, ID: str, stu_Num: int):
        self.list_student = [Student.student_modle()]
        self.list_atom = [Exam_atom.atom_modle(None)]
        self.exam_stage = 0
        self.Name = Name
        self.ID = ID
        self.stu_Num = stu_Num
        self.stu_still = stu_Num
        # 初始化列表
        self.list_student.clear()
        self.list_atom.clear()

    # 根据考生数量分配原子 这里保证传进来的考场时空表要完全正确
    def allocate_atom(self, list_room: Room.Room_TimeSpace):
        # 遍历考场表
        for iRoomVal in list_room.room_cur_list.list_room:
            # 从容量大的教室开始遍历，看看当前人数使用几间教室足够
            # 优化贪心，除数结果保留整数，四射五入
            useRoom = int(min(round(self.stu_still/iRoomVal.room_val), len(iRoomVal.val_list)))
            if useRoom == 0:
                continue
            # 接收分配结果
            iRes = self.solve_atom(useRoom, list_room, iRoomVal)
            # 监考无法满足
            if not iRes:
                return -1
            # 有的教室没装满
            if self.stu_still < 0:
                self.stu_still = 0
                break
        # 改方法处理后，存在教室剩余但学生没分配完的情况，属于货币问题的弊端，利用reverse函数优化
        return self.stu_still

    # 反向遍历，解决存在教室剩余但学生没分配完的情况
    def allocate_atom_reverse(self, list_room: Room.Room_TimeSpace):
        # 反向遍历考场表
        for iRoomVal in reversed(list_room.room_cur_list.list_room):
            # 从容量小的教室开始遍历，将剩余的学生进最大努力安排
            # 优化贪心，除数结果向上取整
            useRoom = int(min(math.ceil(self.stu_still/iRoomVal.room_val), len(iRoomVal.val_list)))
            if useRoom == 0:
                continue
            # 接收分配结果
            iRes = self.solve_atom(useRoom, list_room, iRoomVal)
            # 监考无法满足
            if not iRes:
                return -1
            # 有的教室没装满
            if self.stu_still < 0:
                self.stu_still = 0
                break
        return self.stu_still

    # 处理教室分配，更新剩余学生数，解耦优化
    def solve_atom(self, useRoom: int, list_room: Room.Room_TimeSpace, iRoomVal: Room.Room_Value):
        self.stu_still -= useRoom*iRoomVal.room_val
        list_room.room_cur_list.num_of_all -= useRoom
        while useRoom:
            iAtom = Exam_atom.atom_modle(iRoomVal.val_list[0])
            iAtom.time = list_room.curTime
            # 存在老师不够用问题，弃用此列表
            if not self.allocate_teacher(iAtom, list_room.teacher_can_use):
                return False
            iRoomVal.val_list.remove(iRoomVal.val_list[0])
            self.list_atom.append(iAtom)
            iAtom.num_student = iRoomVal.room_val
            if self.stu_still < 0:
                iAtom.num_student += self.stu_still
            useRoom -= 1
        return True

    # 为原子分配考生
    def allocate_student(self):
        for iAtom in self.list_atom:
            while iAtom.num_student > 0:
                index_student = random.randint(0, len(self.list_student)-1)
                iAtom.arrange_seat(self.list_student[index_student])
                self.list_student.remove(self.list_student[index_student])
        return True

    # 学生列表新增, push
    def push_student(self, student: Student.student_modle):
        self.list_student.append(student)

    # 分配监考老师
    def allocate_teacher(self, iAtom: Exam_atom.atom_modle, teacher_file: Teacher.teacher_list):
        # 这个时间段出现老师不够用的情况了，导致这个时间段不能继续安排考试
        if len(teacher_file.list_teacher) < iAtom.Room.needTeacher:
            return False
        idx = 0
        while idx < len(teacher_file.list_teacher):
            if iAtom.Room.needTeacher <= 0:
                break
            # 冲突检测
            if iAtom.Room.needTeacher == 0:
                break
            if not conflict_ditect.isConflict_repeat_Teacher(teacher_file.list_teacher[idx], teacher_file.list_teacher):
                idx += 1
                continue
            # 优先安排本课程老师
            if self.Name == teacher_file.list_teacher[idx].course:
                iAtom.Room.needTeacher -= 1
                iAtom.list_teacher.append(teacher_file.list_teacher[idx])
                teacher_file.list_teacher.remove(teacher_file.list_teacher[idx])
            else:
                idx += 1
        # 本课程老师不够了，用其他科目的顶替
        while iAtom.Room.needTeacher > 0:
            iAtom.Room.needTeacher -= 1
            iAtom.list_teacher.append(teacher_file.list_teacher[0])
            teacher_file.list_teacher.remove(teacher_file.list_teacher[0])
        return True
