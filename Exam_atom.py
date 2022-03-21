# -*- coding: UTF-8 -*-
import random
import Room
import Student
import Teacher
import conflict_ditect


class atom_modle:

    def __init__(self, iRoom: Room.Room_modle):
        self.num_student = 0
        self.time = ''
        self.conflict_check = []
        self.list_teacher = [Teacher.teacher_modle()]
        self.list_student = [Student.student_modle()]
        self.list_seat = [Student.student_seat(None, None)]
        self.list_seat.clear()
        self.list_teacher.clear()
        self.list_student.clear()
        self.Room = iRoom
        self.cursor_seat = 1

    def arrange_seat(self, student: Student.student_modle):
        iNum = self.cursor_seat
        if conflict_ditect.isConflict_seat(iNum, self.conflict_check):
            return False
        self.conflict_check.append(iNum)
        if conflict_ditect.isConflict_repeat_student(student, self.list_student):
            return False
        iSeat = Student.student_seat(iNum, student)
        self.cursor_seat += 1
        self.list_student.append(student)
        self.list_seat.append(iSeat)
        self.num_student -= 1
        return True
