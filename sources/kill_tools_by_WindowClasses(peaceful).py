import psutil
import win32gui
import win32process
import os, time
import re
from collections import defaultdict
while True:
    def get_all_visible_window_classes_by_pid():
        results_by_pid = defaultdict(list)
        all_accessible_pids = {proc.info['pid'] for proc in psutil.process_iter(['pid'])}

        def enum_windows_callback(hwnd, lparam):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    if pid in all_accessible_pids:
                        class_name = win32gui.GetClassName(hwnd)
                        if class_name not in results_by_pid[pid]:
                            results_by_pid[pid].append(class_name)
                except (win32gui.error, psutil.AccessDenied):
                    pass
            return True

        win32gui.EnumWindows(enum_windows_callback, 0)
        return {pid: classes for pid, classes in results_by_pid.items() if classes}


    window_data = get_all_visible_window_classes_by_pid()
    if not window_data:
        print("Не найдено ни одного видимого окна для сканирования.")

    print("Найдена привязка классов окон для процессов:")
    for pid, classes in window_data.items():
        try:
            p = psutil.Process(pid)
            proc_name = p.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            proc_name = f"PID {pid} (Недоступен/Системный)"

        print(f"Процесс: {proc_name} (PID: {pid})")
        for class_name in classes:
            print(f"  - Класс: {class_name}")

            # Проверка на подозрительный класс окна
            if class_name == "WindowsForms10.Window.8.app.0.3e799b_r8_ad1" or class_name == "oQE3gv8s9LRr0":
                print(f'НАЙДЕН SU ИЛИ prochacker!!! Убийство процесса {proc_name}')
                try:
                    p.kill()
                    # Добавление ловушки в реестр, с осторожностью:
                    #os.system(f'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{proc_name}" /v Debugger /t REG_SZ /d "%temp%\\debuger.exe" /f')
                except Exception as e:
                    print(f"Ошибка при убийстве процесса или изменении реестра: {e}")

            # Проверка на подозрительный класс окна
            if class_name == "Explorer++" or class_name == "TTOTAL_CMD":
                print(f'НАЙДЕН Explorer++ ИЛИ TOTAL_CMD!!! Убийство процесса {proc_name}')
                try:
                    p.kill()
                    # Добавление ловушки в реестр, с осторожностью:
                    #os.system(f'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{proc_name}" /v Debugger /t REG_SZ /d "%temp%\\debuger.exe" /f')
                except Exception as e:
                    print(f"Ошибка при убийстве процесса или изменении реестра: {e}")


            autoruns_patterns = [
                r"^ATL:.*",  # пример шаблона
                r".*Autoruns.*",
            ]

            def is_autoruns_class(class_name):
                for pattern in autoruns_patterns:
                    if re.match(pattern, class_name, re.IGNORECASE):
                        return True
                return False
            
            autoruns_patterns = [
            r"^ATL:.*",  # пример шаблона
            r".*Autoruns.*",
            ]
            
            def is_autoruns_class(class_name):
                for pattern in autoruns_patterns:
                    if re.match(pattern, class_name, re.IGNORECASE):
                        return True
                return False

        
            if is_autoruns_class(class_name):
                print(f'НАЙДЕН Autoruns!!! Убийство процесса {proc_name}')
                try:
                    p.kill()
                    #os.system(f'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{proc_name}" /v Debugger /t REG_SZ /d "%temp%\\debuger.exe" /f')
                except Exception as e:
                    print(f"Ошибка при убийстве процесса: {e}")

            if class_name == "PROCEXPLORER" or class_name == "WinRarWindow":
                print(f'НАЙДЕН PROCESS EXPLORER!!! Убийство процесса {proc_name}')
                try:
                    p.kill()
                    # Добавление ловушки в реестр, с осторожностью:
                    #os.system(f'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{proc_name}" /v Debugger /t REG_SZ /d "%temp%\\debuger.exe" /f')
                except Exception as e:
                    print(f"Ошибка при убийстве процесса или изменении реестра: {e}")

            
    time.sleep(1)