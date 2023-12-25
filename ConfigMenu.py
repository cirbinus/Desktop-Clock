import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QFormLayout,
    QCheckBox,QFontComboBox,QSpinBox,QDoubleSpinBox,QApplication
)
from PySide6.QtGui import QGuiApplication
from configparser import ConfigParser 
from os import path,getenv

def get_config_path():
    if getattr(sys, 'DesktopClock', False):  # 判断是否是单个exe
        # 获取系统appdata目录
        base_path = getenv('LOCALAPPDATA')
    else:
        # 获取当前文件所在的目录
        base_path = path.dirname(path.abspath(__file__))

    # 拼接配置文件的路径
    config_path = path.join(base_path, 'clockConfig.ini')
    return config_path

config_path = get_config_path()
conf1 = ConfigParser()  # 需要实例化一个ConfigParser对象
conf1.read(config_path, encoding='GB18030')

class ConfigMenu(QWidget):
    def __init__(self):
        super(ConfigMenu, self).__init__() # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("Configuration")
        self.setMaximumWidth(100)
        self.center()
        self.font_label = QLabel("Font:", self) # self是指定的父类ConfigMenu，表示QLabel属于ConfigMenu窗口
        self.fontsize_label = QLabel("Fontsize:", self)
        self.color_label = QLabel("Color:",self)
        self.background_label = QLabel("Background:",self)
        self.opacity_label = QLabel("Opacity:",self)

        self.font_line = QFontComboBox(self)
        self.font_line.setMaximumWidth(150)
        self.fontsize_line = QSpinBox(self)
        self.fontsize_line.setRange(0,1000)
        self.color_line = QLineEdit(self)
        self.background_line  = QLineEdit(self)
        self.opacity_line  = QDoubleSpinBox(self)
        self.opacity_line.setRange(0.0,1.0)
        self.opacity_line.setSingleStep(0.1)
        self.opacity_line.setDecimals(2)
        self.isontop_line = QCheckBox(self)
        self.isontop_line.setText("Ontop")
        self.isontop_line.setChecked(True)
        self.isbold_line = QCheckBox(self)
        self.isbold_line.setText("Bold")
        self.isbold_line.setChecked(True)
        self.isframe_line = QCheckBox(self)
        self.isframe_line.setText("Frame")
        self.confirm_button = QPushButton("Confirm")
        
        self.f_layout = QFormLayout() # 实例化一个QFormLayout对象
        self.f_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.f_layout.addRow(self.font_label, self.font_line) # 左边放文本控件，右边放输入型控件
        self.f_layout.addRow(self.fontsize_label, self.fontsize_line)
        self.f_layout.addRow(self.color_label, self.color_line)
        self.f_layout.addRow(self.background_label, self.background_line)
        self.f_layout.addRow(self.opacity_label, self.opacity_line)
        self.f_layout.addRow(self.isbold_line)
        self.f_layout.addRow(self.isontop_line,self.isframe_line)
        self.f_layout.addRow(self.confirm_button)

        self.setLayout(self.f_layout) # 调用窗口的setLayout方法将总布局设置为窗口的整体布局
        self.readConfig()
    
    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


    def readConfig(self):
        # self.x0 = conf1.getint('location', 'x')
        # self.y0 = conf1.getint('location', 'y')
        self.font_line.setCurrentFont(conf1.get('config', 'font'))
        self.fontsize_line.setValue(conf1.getint('config', 'fontsize'))
        self.color_line.setText(conf1.get('config', 'color'))
        self.background_line.setText(conf1.get('config', 'background'))
        self.opacity_line.setValue(conf1.getfloat('config', 'opacity'))
        if conf1.getint('config', 'isontop') == 2:
            self.isontop_line.setChecked(True)
        else:
            self.isontop_line.setChecked(False)

        if conf1.getint('config', 'isbold') == 2:
            self.isbold_line.setChecked(True)
        else:
            self.isbold_line.setChecked(False)

        if conf1.getint('config', 'isframe') == 2:
            self.isframe_line.setChecked(True)
        else:
            self.isframe_line.setChecked(False)


    def writeConfig(self):
        # conf1.set("location","x",str(self.x0))
        # conf1.set("location","y",str(self.y0))
        conf1.set("config","isOnTop",str(self.isontop_line.checkState().value))
        conf1.set("config","font",self.font_line.currentFont().family())
        conf1.set("config","fontSize",str(self.fontsize_line.value()))
        conf1.set("config","isbold",str(self.isbold_line.checkState().value))
        conf1.set("config","color",self.color_line.text())
        conf1.set("config","Opacity",str(self.opacity_line.value()))
        conf1.set("config","background",self.background_line.text())
        conf1.set("config","isFrame",str(self.isframe_line.checkState().value))
        with open(config_path,'w') as cfg:
                conf1.write(cfg) 
                cfg.close()
        print("saved")
        self.close()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    configMenu = ConfigMenu()
    configMenu.show()
    sys.exit(app.exec_())