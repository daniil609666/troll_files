from ctypes import windll
import time
def rep():
    time.sleep(0.2)
    # получаем дескриптор панели задач
    h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
    # скрываем панель задач
    windll.user32.ShowWindow(h, 0)
    time.sleep(0.2)
    # снова показываем панель задач
    windll.user32.ShowWindow(h, 9)
    rep()
rep()