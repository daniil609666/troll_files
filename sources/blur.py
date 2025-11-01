import random, win32con
from win32gui import *
from win32api import *
from math import *
x = GetSystemMetrics(0)
y = GetSystemMetrics(1)



def blur():
    while True:
        hdc = GetDC(0)
        memdc = CreateCompatibleDC(hdc)
        hbit = CreateCompatibleBitmap(hdc, x, y)
        sel = SelectObject(memdc, hbit)

        # Исправлено: теперь функция BitBlt() вызывается с правильным количеством аргументов.
        BitBlt(memdc, 0, 0, x, y, hdc, 0, 0, win32con.SRCCOPY) #копирует содержимое hdc в memdc

        AlphaBlend(hdc, random.randint(-10, 10), random.randint(-10, 10), x, y, memdc, 0, 0, x, y, (0,0,70,0))
        SelectObject(memdc, sel) #возвращает старый объект (hbit)

        DeleteObject(sel) #удалять sel не нужно, тк это возвращенный объект (hbit), который нужно удалить
        DeleteObject(hbit)
        DeleteDC(memdc) #нужно удалять контекст memdc
        ReleaseDC(0,hdc) #освободить hdc


blur()