import win32con
import win32gui
import ctypes
import random
import time

while True:
    rand = random.randint(1, 2)
    #change system cursor
    try:
        cursor = win32gui.LoadImage(0, f"{rand}.ani", win32con.IMAGE_CURSOR, 
                                    0, 0, win32con.LR_LOADFROMFILE)
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)
    except:
        pass
    time.sleep(1)
