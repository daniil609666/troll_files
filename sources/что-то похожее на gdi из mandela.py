import win32api
import win32gui
import win32con
import ctypes
from random import *
import random
from time import sleep
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
desktop = win32gui.GetDesktopWindow()
hdc = win32gui.GetDC(0)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
hdc = win32gui.GetWindowDC(desktop)
sw = win32api.GetSystemMetrics(0)
sh = win32api.GetSystemMetrics(1)
desk = win32gui.GetDC(0)
desc = win32gui.GetDC(0)
xx = win32api.GetSystemMetrics(0)
yy = win32api.GetSystemMetrics(1)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
hdc = win32gui.GetDC(0)
while True:
    try:
        color = randint(10, 100)
        hdc = win32gui.GetDC(0)
        color = color, color, color
        brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
        win32gui.SelectObject(hdc, brush)
        win32gui.BitBlt(hdc, random.randint(-10, 10), random.randint(-10, 10), sw, sh, hdc, 0, 0, win32con.PATINVERT)
        x = y = 0
        x = x + 30
        if x >= w:
            y = y + 30
            x = 0
        if y >= h:
            x = y = 0
        brush = win32gui.CreateSolidBrush(win32api.RGB(
        randrange(255),
        randrange(255),
        randrange(255),
        ))
        win32gui.DeleteObject(brush)
        win32gui.SelectObject(desc, brush)
        sleep(0.1)

    except:
        pass