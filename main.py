# -*- coding: UTF-8 -*-
# @FILE: main.py
# @BRIEF: 入口，可视化
# @version debug 1.5
import tkinter
from tkinter import filedialog, Label, LabelFrame, Entry, Button, StringVar, IntVar, Checkbutton, messagebox, ttk
import Arrange
from tkinter.filedialog import askdirectory
import DBcon

root = tkinter.Tk()
root.geometry("500x400")
root.title("沈航考试安排系统v1.5 Debug")
path_student = tkinter.StringVar()
path_teacher = tkinter.StringVar()
path_course = tkinter.StringVar()
path_room = tkinter.StringVar()
path_option = tkinter.StringVar()
path_early = tkinter.StringVar()
path_middle = tkinter.StringVar()
path_end = tkinter.StringVar()
name_exam = tkinter.StringVar()
d_path = tkinter.StringVar()


def upLoad_student():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_student.set(path_)


def upLoad_teacher():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_teacher.set(path_)


def upLoad_course():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_course.set(path_)


def upLoad_room():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_room.set(path_)


def upLoad_option():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_option.set(path_)


def upLoad_early():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_early.set(path_)


def upLoad_middle():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_middle.set(path_)


def upLoad_end():
    path_ = tkinter.filedialog.askopenfilename()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path_end.set(path_)


def path_up():
    path_ = askdirectory()
    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    d_path.set(path_)


def start():
    if name_exam.get() is None or path_student.get() is None or path_teacher.get() is None or path_course.get() is None or path_early.get() is None or path_middle.get() is None or path_end.get() is None or path_room.get() is None or path_option.get() is None:
        return
    ok = Arrange.enter(name_exam.get(), path_student.get(), path_teacher.get(), path_course.get(),
                       path_early.get(), path_middle.get(), path_end.get(), path_room.get(), path_option.get(),
                       d_path.get())
    if ok < 1:
        if ok == -1:
            messagebox.showinfo(message="期末考试所提供的资源不足")
        elif ok == -2:
            messagebox.showinfo(message="第二阶段考试提供的资源不足")
        elif ok == -3:
            messagebox.showinfo(message="第一阶段考试提供的资源不足")
        else:
            messagebox.showinfo(message="未知错误")
    else:
        newWindow = tkinter.Toplevel(root)
        newWindow.geometry("1600x900")
        tree = ttk.Treeview(newWindow)  # #创建表格对象
        # tree.winfo_geometry("1600x900")
        tree["columns"] = ("学号", "学生姓名", "考试阶段", "课程号", "课程名称", "考试时间", "监考老师工号", "监考老师姓名", "考场号", "座位号")
        tree.column("学号", width=100)  # #设置列
        tree.column("学生姓名", width=100)
        tree.column("考试阶段", width=100)
        tree.column("课程号", width=100)
        tree.column("课程名称", width=100)
        tree.column("考试时间", width=100)
        tree.column("监考老师工号", width=500)
        tree.column("监考老师姓名", width=300)
        tree.column("考场号", width=100)
        tree.column("座位号", width=100)

        tree.heading("学号", text="学号")  # #设置显示的表头名
        tree.heading("学生姓名", text="学生姓名")
        tree.heading("考试阶段", text="考试阶段")
        tree.heading("课程号", text="课程号")
        tree.heading("课程名称", text="课程名称")
        tree.heading("考试时间", text="考试时间")
        tree.heading("监考老师工号", text="监考老师工号")
        tree.heading("监考老师姓名", text="监考老师姓名")
        tree.heading("考场号", text="考场号")
        tree.heading("座位号", text="座位号")

        conn = DBcon.getConnection('localhost', 'root', 'gefu1128', name_exam.get(), 'utf8')
        cs1 = conn.cursor()
        sql = "select * from book_result"
        cs1.execute(sql)
        alldata = cs1.fetchall()
        idx = 1
        for idata in alldata:
            tree.insert("", idx, text="line{}".format(idx), values=(
                idata[0], idata[1], idata[2], idata[3], idata[4], idata[5], idata[6], idata[7], idata[8], idata[9]))

        tree.pack()
        cs1.close()
        conn.close()


# 学生表路径
tkinter.Label(root, text="学生表路径:").grid(row=0, column=0)
tkinter.Entry(root, textvariable=path_student).grid(row=0, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_student).grid(row=0, column=2)

# 教师表路径
tkinter.Label(root, text="教师表路径:").grid(row=1, column=0)
tkinter.Entry(root, textvariable=path_teacher).grid(row=1, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_teacher).grid(row=1, column=2)

# 课程表路径
tkinter.Label(root, text="课程表路径:").grid(row=2, column=0)
tkinter.Entry(root, textvariable=path_course).grid(row=2, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_course).grid(row=2, column=2)

# 考场表路径
tkinter.Label(root, text="考场表路径:").grid(row=3, column=0)
tkinter.Entry(root, textvariable=path_room).grid(row=3, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_room).grid(row=3, column=2)

# 选修表路径
tkinter.Label(root, text="选修表路径:").grid(row=4, column=0)
tkinter.Entry(root, textvariable=path_option).grid(row=4, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_option).grid(row=4, column=2)

# 期末安排路径
tkinter.Label(root, text="期末安排路径:").grid(row=5, column=0)
tkinter.Entry(root, textvariable=path_end).grid(row=5, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_end).grid(row=5, column=2)

# 第二次阶段安排路径
tkinter.Label(root, text="第二次阶段安排路径:").grid(row=6, column=0)
tkinter.Entry(root, textvariable=path_middle).grid(row=6, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_middle).grid(row=6, column=2)

# 第一次阶段安排路径
tkinter.Label(root, text="第一次阶段安排路径:").grid(row=7, column=0)
tkinter.Entry(root, textvariable=path_early).grid(row=7, column=1)
tkinter.Button(root, text="路径选择", command=upLoad_early).grid(row=7, column=2)

# 考试名称
tkinter.Entry(root, textvariable=name_exam).grid(row=8, column=1)

# 路径
tkinter.Label(root, text="输出路径:").grid(row=9, column=0)
tkinter.Entry(root, textvariable=d_path).grid(row=9, column=1)
tkinter.Button(root, text="路径选择", command=path_up).grid(row=9, column=2)

# 开始按钮
tkinter.Button(root, text="安排考试", command=start).grid(row=14, column=1)

# 启动
root.mainloop()
