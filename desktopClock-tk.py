#!/usr/local/python39/bin/python3.9
from time import strftime
from tkinter import Label, mainloop
import tkinter as tk
from random import randint
from os import path, mkdir

if path.exists('./Config/') == False:
    mkdir('./Config/')


class DragWindow(tk.Tk):
    root_x, root_y, abs_x, abs_y = 0, 0, 0, 0
    width, height = None, None

    def __init__(self, topmost=True, alpha=0.4, bg="gray", width=None, height=None):
        super().__init__()
        self["bg"] = bg
        self.width, self.height = width, height
        self.overrideredirect(True)
        self.wm_attributes("-alpha", 0.0)      # 透明度
        # self.wm_attributes('-type', 'dock')  # 置为工具窗口
        self.wm_attributes("-topmost", topmost)  # 永远处于顶层
        self.bind('<B1-Motion>', self._on_move)
        self.bind('<ButtonPress-1>', self._on_tap)

    def set_display_postion(self, offset_x, offset_y):
        self.geometry("+%s+%s" % (offset_x, offset_y))

    def set_window_size(self, w, h):
        self.width, self.height = w, h
        self.geometry("%sx%s" % (w, h))

    def _on_move(self, event):
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        if self.width and self.height:
            geo_str = "%sx%s+%s+%s" % (self.width, self.height,
                                       self.abs_x + offset_x, self.abs_y + offset_y)
        else:
            geo_str = "+%s+%s" % (self.abs_x + offset_x, self.abs_y + offset_y)
        # 记录窗口最后停留的位置
        file = open('./Config/state.txt', 'w')
        file.seek(0)
        file.truncate()
        now_state = geo_str.split('+')
        file.write(now_state[1]+" "+now_state[2])
        file.close()

        self.geometry(geo_str)

    def _on_tap(self, event):
        self.root_x, self.root_y = event.x_root, event.y_root  # 窗口左上角到鼠标的坐标
        self.abs_x, self.abs_y = self.winfo_x(), self.winfo_y()  # 窗口左上角到显示器左上角的坐标


root = DragWindow()
root.resizable()
color = "white"

# 界面有多大，完全是靠字体撑起来的， 背景是黑色， 字体是白色
lbl = Label(root, font=("arial", 60, "bold"), fg=color, bg="black")
lbl.pack(anchor="center", fill="both", expand=1)


def showtime():
    string = strftime("%H:%M:%S")

    lbl.config(text=string)
    lbl.after(10, showtime)       # 1秒钟以后执行time函数
    # 读取上次窗口位置
    if path.exists('./Config/state.txt'):
        file = open('./Config/state.txt', 'r')
        old_state = file.read().split(" ")
        offset_x, offset_y = old_state[0], old_state[1]
        # width, height = root.winfo_width(), root.winfo_height()
        file.close()
        geo_str = "+%s+%s" % (offset_x, offset_y)
        root.geometry(geo_str)
    if path.exists('./Config/color.txt'):
        file1 = open('./Config/color.txt', 'r')
        value = file1.read()
        if value != '':
            global color
            color = value
        # width, height = root.winfo_width(), root.winfo_height()
        file1.close()
    lbl.config(foreground=color)


def mouse_click(event):
    global color
    color = f"#{randint(0,16777215):06x}"
    lbl.config(foreground=color)
    file1 = open('./Config/color.txt', 'w')
    file1.seek(0)
    file1.truncate()
    file1.write(color)
    file1.close()


def close(event):
    root.destroy()


lbl.bind("<Double-Button-1>", mouse_click)
lbl.bind("<Double-Button-3>", close)
showtime()

mainloop()
