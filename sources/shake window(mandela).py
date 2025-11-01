import win32gui
import random
import time
import sys

sys.setrecursionlimit(999999)

def move_windows():
    count = 0
    while True:
        count += 1
        print(count)
        
        def callback(hwnd, extra):
            nonlocal count
            
            # Определяем, нужна ли задержка
            should_delay = count <= 40
            
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            
            try:
                if win32gui.IsWindowVisible(hwnd):
                    rand_x = random.randint(-20, 20)
                    rand_y = random.randint(-10, 10)
                    
                    new_x = max(0, x + rand_x)
                    new_y = max(0, y + rand_y)
                    
                    win32gui.MoveWindow(hwnd, new_x, new_y, w, h, True)
                    
                    # Добавляем задержку только для первых 40 итераций
                    if should_delay:
                        time.sleep(0.01)
                        
            except Exception as e:
                pass
                
            return True
        
        win32gui.EnumWindows(callback, None)

if __name__ == "__main__":
    move_windows()