#!/data/home/zhou/codes/python3/bin/python3
from PySide6.QtWidgets import QLabel, QApplication, QGraphicsOpacityEffect, QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtGui import QFont, QCursor,QShortcut
from PySide6.QtCore import QTimer, QDateTime, Qt,QCoreApplication
from random import randint
from os import path,chdir,getenv
import sys,subprocess
from configparser import ConfigParser

def get_config_path():
    # if 'python.exe' in sys.executable:  # 判断是否是单个exe
    #     # 获取当前文件所在的目录
    #     base_path = path.dirname(path.abspath(__file__))
    # else:
    #     # 获取系统appdata目录
    #     try:
    #         base_path = getenv('APPDATA')
    #     except:
    #         base_path = "/home/clock/"
    try:
        base_path = getenv('LOCALAPPDATA')
    except:
        base_path = "/home/clock/"

    # 拼接配置文件的路径
    location_path = path.join(base_path, 'clockLocation.ini')
    config_path = path.join(base_path, 'clockConfig.ini')
    return [location_path,config_path]


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
        self.m_flag = None
        self.w = None
        # 透明窗口
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置需要记录的值
        self.x, self.y = 0, 0
        self.isOnTop = 2
        self.font = "Arial"
        self.fontSize = 55
        self.isbold = 2
        self.color = "#fff"
        self.background = "#0B0E11"
        self.isFrame = 0
        self.setPanel()

    def initConfig(self):
        self.locat = ConfigParser() 
        self.locat.read(location_path, encoding='GB18030')
        conf.read(config_path, encoding='GB18030')
        # 第一次运行生成config文件,后面获取配置文件
        if path.exists(config_path) == False and path.exists(location_path) == False:
            print("creat ini")
            self.locat["location"] = {
                "x" : 0,
                "y" : 0,
                }
            conf["config"] = {
                "isOnTop" : self.isOnTop,
                "font" :self.font,
                "fontSize" : self.fontSize,
                "isbold" : self.isbold,
                "color" : self.color,
                "Opacity" : 0.8,
                "background" : self.background,
            }
            with open(config_path,'w') as cfg:
                conf.write(cfg) 
                cfg.close()
            with open(location_path,'w') as cfg:
                self.locat.write(cfg) 
                cfg.close()

        else:
            self.x, self.y = self.locat.getint("location", "x"), self.locat.getint("location", "y")
            self.isOnTop = conf.getint('config', 'isOnTop')
            self.font = conf.get('config', 'font')
            self.fontSize = conf.getint('config', 'fontSize')
            self.isbold = conf.getint('config', 'isbold')
            self.color = conf.get('config', 'color')
            self.background = conf.get('config', 'background')
            self.opacity = conf.getfloat('config', 'Opacity')

    def setPanel(self):
        print("开始设置")
        self.initConfig()
         # 设置窗体无边框和置顶
        if self.isOnTop == 2:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        elif self.isOnTop == 0:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # 设置字体
        lbl.setFont(QFont(self.font, self.fontSize,QFont.Bold))
        lbl.setStyleSheet(f"background-color: {self.background};")
        # 是否加粗
        if self.isbold == 0:
            lbl.setFont(QFont(self.font, self.fontSize))
        # 检查颜色
        changeLabelColor(self.color,self.background)
        # 检查透明度
        op.setOpacity(self.opacity) 
        # 检查坐标
        self.adjustSize()
        self.setVisible(True)  # 设置可见，避免坐标默认为（0，0）
        print(self.x, self.y)
        self.setGeometry(self.x, self.y,100,50)
        
    
    def mousePressEvent(self, event):
        # 单击
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
        elif event.button() == Qt.MiddleButton:
            # 中键退出所有程序
             sys.exit(app.exec())
        elif event.button() == Qt.RightButton:
            # 右键配置界面
            from ConfigMenu import ConfigMenu
            self.w = ConfigMenu()
            self.w.confirm_button.clicked.connect(self.w.writeConfig)
            self.w.confirm_button.clicked.connect(self.setPanel)
            self.w.show()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos()-self.m_Position)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        # 记录窗口最后停留的位置
        self.locat["location"]["x"] = str(self.geometry().left())
        self.locat["location"]["y"] = str(self.geometry().top())
        o = open(location_path, 'w')
        self.locat.write(o)
        o.close()#不要忘记关闭

    def mouseDoubleClickEvent(self, event):
        # 双击变色
        if event.button() == Qt.LeftButton:
            self.color = f"#{randint(0,16777215):06x}"
            conf["config"]["color"] = self.color
            o = open(config_path, 'w')
            conf.write(o)
            o.close()#不要忘记关闭
            changeLabelColor(self.color,self.background)
    
    # 重启主程序
    def restart_application(self):
        app = QCoreApplication.instance()
        app.quit()
        self.initConfig()
        self.setPanel()
        subprocess.call([sys.executable] + sys.argv)

if __name__ == '__main__':
    
    config_path = get_config_path()[1]
    location_path = get_config_path()[0]
    currentDir = path.dirname(path.abspath(__file__))
    chdir(currentDir) 
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    op = QGraphicsOpacityEffect() # 透明对象
    if path.exists(config_path):
        conf.read(config_path, encoding='GB18030')
        opacity = conf.getfloat('config', 'Opacity')
    else:
        opacity = 0.8

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    lbl = QLabel()
    lbl.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
    lbl.setAlignment(Qt.AlignCenter) #  文本居中
    # lbl.adjustSize()
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
    sys.exit(app.exec())
