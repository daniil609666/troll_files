import ctypes
import time
def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

def change_wallpaper():
    images = [f"%temp%\\{i}.png" for i in range(1, 11)]#если надо поставить 10 обоев по очереди то ставим 11
    for image in images:
        set_wallpaper(image)
        time.sleep(1)
def repit():
    change_wallpaper()
    repit()
repit()