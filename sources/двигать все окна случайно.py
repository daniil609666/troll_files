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

# Get list of all windows
windows_list = get_all_window_titles()

# move the windows
def move_windows(windows):
    for hwnd, title in windows:
        randx = random.randint(0, 1920)
        randy = random.randint(0, 1080)
        win32gui.MoveWindow(hwnd, randx, randy, randx, randy, True)

# Call the move_windows function on repeat
while True:
    try:
        windows_list = get_all_window_titles()
        move_windows(windows_list)
        print(windows_list)
        #time.sleep(2)
    except pywintypes.error as e:
        print(f"PyWinTypes Error in main loop:")
        print(f"Error details: {e}")
        pass
