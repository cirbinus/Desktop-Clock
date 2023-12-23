#!venv/bin/python
from PySide6.QtWidgets import QLabel, QApplication, QGraphicsOpacityEffect, QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtGui import QFont, QCursor
from PySide6.QtCore import QTimer, QDateTime, Qt
from my_window_effect  import WindowEffect
from random import randint
from os import path,chdir
import sys
from configparser import ConfigParser 

currentDir = path.dirname(path.abspath(__file__))
chdir(currentDir) 
conf = ConfigParser()  # 需要实例化一个ConfigParser对象
op = QGraphicsOpacityEffect() # 透明对象

if path.exists('./config.ini'):
    conf.read('./config.ini', encoding='GB18030')
    opacity = conf.getfloat('config', 'Opacity')
else:
    opacity = 0.8


def showtime():
    datetime = QDateTime.currentDateTime().time()
    text = datetime.toString()
    lbl.setText(text)

def changeLabelColor(color,background):
    lbl.setStyleSheet(f"""
                background-color: {background};
                border-radius:10px;    /*设置圆角半径 */
                padding:2px 4px;  /*QFrame边框与内部其它部件的距离*/
                color: {color};
            """)


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        # 透明窗口
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置需要记录的值
        self.x, self.y, self.isOnTop = 0, 0, 1
        self.font = "arial"
        self.fontSize = 55
        self.isbold = 1
        self.color = "#fff"
        self.background = "#0B0E11"
        self.isFrame = 0
        # 第一次运行生成config文件,后面获取配置文件
        if path.exists('./config.ini') == False:
            conf["config"] = {
                "x" : self.x,
                "y" : self.y,
                "isOnTop" : self.isOnTop,
                "font" :self.font,
                "fontSize" : self.fontSize,
                "isbold" : self.isbold,
                "color" : self.color,
                "Opacity" : 0.8,
                "background" : self.background,
                "isFrame" : self.isFrame,
            }
            with open('./config.ini','w') as cfg:
                conf.write(cfg) 
                cfg.close()
        else:
           print(conf.items('config')) 
           self.x, self.y, self.isOnTop = conf.getint('config', 'x'), conf.getint('config', 'y'), conf.getint('config', 'isOnTop')
           self.font = conf.get('config', 'font')
           self.fontSize = conf.getint('config', 'fontSize')
           self.isbold = conf.getint('config', 'isbold')
           self.color = conf.get('config', 'color')
           self.background = conf.get('config', 'background')
           self.isFrame = conf.getint('config', 'isFrame')

         # 设置窗体无边框和置顶
        if self.isOnTop == 1:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        elif self.isOnTop == 0:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # 设置字体
        lbl.setFont(QFont(self.font, self.fontSize,QFont.Bold))
        lbl.setStyleSheet(f"background-color: {self.background};")
        # 毛玻璃风格边框
        if self.isFrame == 1:
            self.windowEffect = WindowEffect()
            self.setStyleSheet("background:transparent")
            self.windowEffect.setAcrylicEffect(int(self.winId()))
        # 是否加粗
        if self.isbold == 0:
            lbl.setFont(QFont(self.font, self.fontSize))
        # 检查颜色
        changeLabelColor(self.color,self.background)
        # 检查坐标
        self.setGeometry(self.x, self.y,100,50)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
        if event.button() == Qt.MiddleButton:
            if self.isOnTop == 0:
                self.isOnTop = 1
                self.setWindowFlags(Qt.FramelessWindowHint |
                                    Qt.WindowStaysOnTopHint | Qt.Tool)
                self.show()
            else:
                self.isOnTop = 0
                self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
                self.show()
            print(self.isOnTop)
            conf['config']["isOnTop"] = str(self.isOnTop)
            o = open('./config.ini', 'w')
            conf.write(o)
            o.close()#不要忘记关闭

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos()-self.m_Position)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        # 记录窗口最后停留的位置
        conf['config']["x"] = str(self.geometry().left())
        conf['config']["y"] = str(self.geometry().top())
        o = open('./config.ini', 'w')
        conf.write(o)
        o.close()#不要忘记关闭

    def mouseDoubleClickEvent(self, event):
        # 双击
        if event.button() == Qt.RightButton:
            self.close()
            sys.exit(app.exec_())
        elif event.button() == Qt.LeftButton:
            self.color = f"#{randint(0,16777215):06x}"
            conf["config"]["color"] = self.color
            o = open('./config.ini', 'w')
            conf.write(o)
            o.close()#不要忘记关闭
            changeLabelColor(self.color,self.background)


app = QApplication(sys.argv)
lbl = QLabel()
lbl.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
lbl.setAlignment(Qt.AlignCenter) #  文本居中
lbl.adjustSize()
op.setOpacity(opacity)  # 透明度
lbl.setGraphicsEffect(op)
lbl.setAutoFillBackground(True)
layout = QVBoxLayout()
layout.addWidget(lbl)


timer = QTimer()
timer.timeout.connect(showtime)
timer.start()

main = MyWidget()
main.setLayout(layout)
main.show()
sys.exit(app.exec_())
