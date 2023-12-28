import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QFormLayout,
    QCheckBox,QFontComboBox,QSpinBox,QDoubleSpinBox,QApplication,QHBoxLayout
)
from PySide6.QtGui import QGuiApplication,Qt
from configparser import ConfigParser 
from os import path,getenv

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
    config_path = path.join(base_path, 'clockConfig.ini')
    return config_path

class ConfigMenu(QWidget):
    def __init__(self):
        super(ConfigMenu, self).__init__() # 使用super函数可以实现子类使用父类的方法
        self.config_path = get_config_path()
        self.conf1 = ConfigParser()  # 需要实例化一个ConfigParser对象
        self.conf1.read(self.config_path, encoding='GB18030')
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
        self.confirm_button = QPushButton("Confirm")
        
        self.f_layout = QFormLayout() # 实例化一个QFormLayout对象
        self.f_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.f_layout.addRow(self.font_label, self.font_line) # 左边放文本控件，右边放输入型控件
        self.f_layout.addRow(self.fontsize_label, self.fontsize_line)
        self.f_layout.addRow(self.color_label, self.color_line)
        self.f_layout.addRow(self.background_label, self.background_line)
        self.f_layout.addRow(self.opacity_label, self.opacity_line)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.isbold_line,alignment= Qt.AlignCenter)
        self.hbox.addWidget(self.isontop_line,alignment= Qt.AlignCenter)
        self.f_layout.addRow(self.hbox)
        self.f_layout.addRow(self.confirm_button)
        self.setLayout(self.f_layout) # 调用窗口的setLayout方法将总布局设置为窗口的整体布局
        self.readConfig()
    
    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


    def readConfig(self):
        self.font_line.setCurrentFont(self.conf1.get('config', 'font'))
        self.fontsize_line.setValue(self.conf1.getint('config', 'fontsize'))
        self.color_line.setText(self.conf1.get('config', 'color'))
        self.background_line.setText(self.conf1.get('config', 'background'))
        self.opacity_line.setValue(self.conf1.getfloat('config', 'opacity'))
        if self.conf1.getint('config', 'isontop') == 2:
            self.isontop_line.setChecked(True)
        else:
            self.isontop_line.setChecked(False)

        if self.conf1.getint('config', 'isbold') == 2:
            self.isbold_line.setChecked(True)
        else:
            self.isbold_line.setChecked(False)


    def writeConfig(self):
        # conf1.set("location","x",str(self.x0))
        # conf1.set("location","y",str(self.y0))
        self.conf1.set("config","isOnTop",str(self.isontop_line.checkState().value))
        self.conf1.set("config","font",self.font_line.currentFont().family())
        self.conf1.set("config","fontSize",str(self.fontsize_line.value()))
        self.conf1.set("config","isbold",str(self.isbold_line.checkState().value))
        self.conf1.set("config","color",self.color_line.text())
        self.conf1.set("config","Opacity",str(self.opacity_line.value()))
        self.conf1.set("config","background",self.background_line.text())
        with open(self.config_path,'w') as cfg:
                self.conf1.write(cfg) 
                cfg.close()
        print("saved")
        self.close()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    configMenu = ConfigMenu()
    configMenu.show()
    sys.exit(app.exec_())