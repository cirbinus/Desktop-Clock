**Read this in other languages: [中文](README_zh.md).**

# Desktop clock

This is a simple, beautiful desktop clock.  
You can drag and change the color and size at will.

<img src="演示.gif" width=400 height=250>

## Running environment

1. Desktop System (WIN10+)  
Windows 11 Pro 23H2  

2. Python version (3.7+)  
Python3.7.4 64-bit  

3. Third-party library: PySide6  
``pip install pyside6``

## Usage

### Basic usage

1. Drag: Hold down the left mouse button.  

2. Switch font color: double-click with the left mouse button.  
 [RGB color picker](https://www.rapidtables.com/web/color/RGB_Color.html)  
3. Open the configuration window: right-click the mouse.  

4. Exit the program: click the middle mouse button.  

### Configuration file
```
x: The distance between the component and the left side of the screen.  
y: The distance between the component and the top of the screen.  
isontop: indicate whether the component is placed ontop.  

font: Set the font.  
fontsize: Set the fontsize, which affects the component display size.  
isbold: Set bold text.  
color: Set the text color.  
background: Set the component background color.  

opacity: Set component transparency.  
```
