**Read this in other languages: [中文](README_zh.md).**

# Desktop clock

This is a simple, beautiful desktop clock.

<img src="show01.png" width=440 height=250>

## Description

1. The desktop clock is developed based on Python3 and Qt6, and the uploaded file contains the TKinter version.
2. Quickly change and save colors, sizes, patterns, etc.
2.Qt6 supports Windows10-11 but does not support Windows XP.
3. The frosted glass rounded background is not yet implemented, but the api is already in the my_window_effect-py file.

## Running environment

1. Desktop System (WIN10+)  
Windows 11 Pro 23H2  

2. Python version (3.7+)  
Python3.7.4 64-bit  

3. Third-party library: PySide6  
``pip install pyside6``

## Usage

### Basic usage

1. Press and hold the left mouse button to drag
2. Double-click the left mouse button to change the font color
3. Click the middle mouse button to determine whether to switch to the top layer
4. Double-click the right mouse button to exit the program

### Configuration file
```
x: The distance between the component and the left side of the screen.  
y: Distance between the component and the top of the screen.  
isontop: indicates whether the component is placed ontop.  

font: Sets the font.  
fontsize: Sets the fontsize, which affects the component display size.  
isbold: Sets bold text.  
color: Sets the text color.  
background: Sets the component background color.  

opacity: Sets component transparency.  
isframe: Sets whether to display a border.  
```
