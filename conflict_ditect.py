# -*- coding: UTF-8 -*-
import Student
import Teacher


def isConflict_seat(i: int, seat_list: list):
    if i in seat_list:
        return True
    else:
        return False


def isConflict_repeat_student(student: Student.student_modle, student_list: list):
    if student in student_list:
        return True
    else:
        return False


def isConflict_repeat_Teacher(teacher: Teacher.teacher_modle, teacher_list: list):
    return True
