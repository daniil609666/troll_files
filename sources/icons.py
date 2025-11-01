import msvcrt
import sys
import time
import random
import pythoncom
import win32com.client as wcomcli
from win32com.shell import shell, shellcon
sys.setrecursionlimit(999999999)

# Константы для работы с Windows Shell
SWC_DESKTOP = 0x08
SWFO_NEEDDISPATCH = 0x01
CLSID_ShellWindows = "{9BA05972-F6A8-11CF-A442-00A0C90A8F39}"
IID_IFolderView = "{CDE725B0-CCC9-4519-917E-325D72FAB4CE}"

def check_position_available(folder_view, items_len, pos, item):
    """
    Проверяет, не перекрывается ли новая позиция с другими иконками
    """
    for i in range(items_len):
        other_item = folder_view.Item(i)
        if other_item != item:
            current_pos = folder_view.GetItemPosition(other_item)
            if abs(current_pos[0] - pos[0]) < 50 and abs(current_pos[1] - pos[1]) < 50:
                return False
    return True

def main():
    # Получаем доступ к окну рабочего стола
    shell_windows = wcomcli.Dispatch(CLSID_ShellWindows)
    hwnd = 0
    dispatch = shell_windows.FindWindowSW(
        wcomcli.VARIANT(pythoncom.VT_I4, shellcon.CSIDL_DESKTOP),
        wcomcli.VARIANT(pythoncom.VT_EMPTY, None),
        SWC_DESKTOP, hwnd, SWFO_NEEDDISPATCH,
    )
    
    # Получаем интерфейс IFolderView для работы с иконками
    service_provider = dispatch._oleobj_.QueryInterface(pythoncom.IID_IServiceProvider)
    browser = service_provider.QueryService(shell.SID_STopLevelBrowser, shell.IID_IShellBrowser)
    shell_view = browser.QueryActiveShellView()
    folder_view = shell_view.QueryInterface(IID_IFolderView)
    
    # Получаем количество элементов на рабочем столе
    items_len = folder_view.ItemCount(shellcon.SVGIO_ALLVIEW)
    
    # Определяем границы рабочего стола
    max_x = 1920  # Ширина экрана
    max_y = 1080  # Высота экрана
    
    # Перебираем все элементы
    for i in range(items_len):
        item = folder_view.Item(i)
        desktop_folder = shell.SHGetDesktopFolder()
        item_name = desktop_folder.GetDisplayNameOf([item], shellcon.SHGDN_NORMAL)
        
        # Находим подходящую случайную позицию
        while True:
            random_pos = (
                random.randint(0, max_x),
                random.randint(0, max_y)
            )
            if check_position_available(folder_view, items_len, random_pos, item):
                break
        
        # Перемещаем иконку
        folder_view.SelectAndPositionItem(item, random_pos, shellcon.SVSI_POSITIONITEM)
        
        # Пауза для визуализации движения
        time.sleep(0.001)

    
def rep():
    try:
        main()
    except Exception as e:
        print(f"\nОшибка: {str(e)}")
        rep()
    rep()
rep()