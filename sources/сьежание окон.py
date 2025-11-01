import win32gui
import random, time
def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))
    try:
        new_x = x+10
        new_y = y+10
        win32gui.MoveWindow(hwnd, new_x, new_y, w, h, True)
    except:
        pass
while True:
    win32gui.EnumWindows(callback, None)
    time.sleep(0.5)
