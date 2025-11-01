import random
from win32gui import *
from win32api import *
from math import *
hwnd = GetDesktopWindow()
hdc2 = GetWindowDC(hwnd)
x = GetSystemMetrics(0)
y = GetSystemMetrics(1)
x2 = GetSystemMetrics(0)
y2 = GetSystemMetrics(1)
desktop = GetDesktopWindow()
left, top, right, bottom = GetWindowRect(desktop)

def radial_move():
    while True:
        hdc = GetDC(0)
        memdc = CreateCompatibleDC(hdc)
        hbit = CreateCompatibleBitmap(hdc, x, y)
        sel = SelectObject(memdc, hbit)

        val = random.randint(1, 2)
        rateofturning=30
        print(val)
        if val == 1:
            PlgBlt(memdc, ((left-rateofturning, top+rateofturning) , (rateofturning, top-rateofturning), (left+rateofturning,  bottom+rateofturning)), hdc, 0, 0, x2, y2, 0, 0, 0)

        if val == 2:
            PlgBlt(memdc, ((left-rateofturning, top+rateofturning) , (rateofturning, top-rateofturning), (left+rateofturning,  bottom+rateofturning)), hdc, 0, 0, x2, y2, 0, 0, 0)

        AlphaBlend(hdc, random.randint(-10, 10), random.randint(-10, 10), x, y, memdc, 0, 0, x, y, (0,0,70,0))

        SelectObject(memdc, sel)

        DeleteObject(sel)
        DeleteObject(hbit)
        DeleteObject(memdc)
        DeleteObject(hdc)

radial_move()