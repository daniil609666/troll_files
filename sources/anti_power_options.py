import os
import time
import psutil

TARGET_NAME = "LogonUI.exe"

while True:
    for p in psutil.process_iter(['pid', 'name', 'create_time', 'exe']):
        try:
            name = (p.info.get('name') or '').lower()
            if name != TARGET_NAME.lower():
                continue

            pid = p.info['pid']
            if pid == os.getpid():
                # Не убиваем сам скрипт, если вдруг он называется так же
                continue

            print(f"Найден {name} (pid={pid}) — пробуем завершить")

            proc = psutil.Process(pid)
            # сначала мягко
            proc.terminate()
            try:
                proc.wait(timeout=3)
                print(f"Процесс {pid} корректно завершён (terminate).")
            except psutil.TimeoutExpired:
                print(f"Процесс {pid} не завершился, пытаемcя kill()")
                proc.kill()
                try:
                    proc.wait(timeout=2)
                    print(f"Процесс {pid} убит (kill).")
                except psutil.TimeoutExpired:
                    print(f"Не удалось убить процесс {pid} в отведённое время.")
        except psutil.NoSuchProcess:
            # Процесс уже ушёл — игнорируем
            pass
        except psutil.AccessDenied:
            print(f"Нет прав для завершения процесса pid={p.info.get('pid')}")
        except Exception as e:
            print(f"Ошибка при обработке процесса: {e}")

    # интервал между проверками — подберите под вашу задачу
    #time.sleep(1.0)
