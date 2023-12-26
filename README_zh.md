**Read this in other languages: [English](README.md).**

# 桌面时钟

这是一个简洁、美观的桌面时钟。可随意拖拽、改变颜色、大小。  

<img src="演示.gif" width=400 height=250>

## 运行环境

1.桌面系统(WIN10+)  
Windows 11 专业版 23H2  

2.Python版本(3.7+)  
Python3.7.4 64-bit  

3.第三方库：PySide6  
``pip install pyside6``

## 用法

### 基本用法

1.拖拽：鼠标左键按住。 

2.切换字体颜色：鼠标左键双击。  
  [RGB颜色代码表](https://www.rapidtables.org/zh-CN/web/color/RGB_Color.html)

3.打开配置窗口：鼠标右键单击。  

4.退出程序：鼠标中键单击。

### 配置文件
```
x：组件与屏幕左边的距离。  
y：组件与屏幕顶部的距离。  
isontop：组件是否置顶。  

font：设置字体。  
fontsize：设置字号，影响组件显示大小。  
isbold：设置文字加粗。  
color：设置文字颜色。  
background：设置组件背景颜色。  

opacity：设置组件透明度。  
isframe：设置是否显示边框。  
```
