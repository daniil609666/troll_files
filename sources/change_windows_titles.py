import win32gui
import random
import pywintypes, time

def get_all_window_titles():
    all_windows = []
    def enum_handler(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        if title:
            all_windows.append((hwnd, title))
    
    win32gui.EnumWindows(enum_handler, None)
    return all_windows


all_windows = get_all_window_titles()

while True:
    all_windows = get_all_window_titles()
    for hwnd, title in all_windows:
        keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '/', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', ':', ' ', '_', '+', '"', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '>', '<', '?', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*']
        title_final = ''.join(random.choice(keys) for _ in range(20 ))  # More efficient title generation
        print(f"Original Title: {title}, New Title: {title_final}") #Added the original title to track the new title.
        try:
            win32gui.SetWindowText(hwnd, title_final)
        except pywintypes.error as e:
            print(f"Error setting window text for handle {hwnd}: {e}")
    #time.sleep(1)