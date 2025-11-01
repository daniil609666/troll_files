import win32gui, random, win32con
import time  # Import the time module

def get_all_window_titles():
    all_windows = []
    def enum_handler(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        if title:
            all_windows.append((hwnd, title))

    win32gui.EnumWindows(enum_handler, None)
    return all_windows

global windows_list
# Get list of all windows
windows_list = get_all_window_titles()

def shake_window(hwnd, shake_duration=3, shake_intensity=10):
    """Трясет окно в течение shake_duration секунд."""
    start_time = time.time()
    while time.time() - start_time < shake_duration:
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]

            rand_x = random.randint(-shake_intensity, shake_intensity)
            rand_y = random.randint(-shake_intensity // 2, shake_intensity // 2) # Reduced vertical intensity

            new_x = max(0, x + rand_x)
            new_y = max(0, y + rand_y)

            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
            #win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.SetActiveWindow(hwnd)
            win32gui.MoveWindow(hwnd, new_x, new_y, w, h, True)
            #time.sleep(0.01)  # Add a small delay to control the shake speed

        except win32gui.error:
            print(f"Window with handle {hwnd} not found or invalid.")
            pass
def find_windows_containing_text(text):
    """Находит дескрипторы окон, содержащих заданный текст в заголовке."""
    window_list = []
    def enum_windows_callback(hwnd, wildcard):
      title = win32gui.GetWindowText(hwnd)
      if text.lower() in title.lower():
        window_list.append(hwnd)
      return True

def find_window_by_title(title):
    """Находит окно по заголовку и возвращает его хэндл."""
    def callback(hwnd, hwnds):
        if title in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
        return True
    

    global hwnds
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        return hwnds[0]  # Возвращаем первое найденное окно
    else:
        return None

def close_window(hwnd):
    """Закрывает окно."""
    try:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    except win32gui.error:
        print(f"Failed to close window with handle {hwnd}.")

while True:
    try:
        windows_list.remove('Program Manager')
        windows_list.remove('Microsoft Text Input Application')
        windows_list.remove('Пуск')
    except:
        pass
    for hwnd, title in windows_list:
        hwnd = find_window_by_title(title)
        if hwnd:
            if win32gui.IsWindowVisible(hwnd):
                print(f"Found window with handle: {hwnd}")

                shake_window(hwnd)  # Shake for 3 second
                print(title)
                windows_list = get_all_window_titles()
                close_window(hwnd)
                print("Window closed.")
        else:
            print(f"Window with title '{title}' not found.")