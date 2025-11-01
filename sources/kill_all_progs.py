import re
import time
import psutil

# Примеры правил игнорирования
ignore_names = {'systemd', 'bash', 'idle', 'python', 'dllhost.exe', 'backgroundTaskHost.exe', 'svchost.exe', 'SDXHelper.exe', 'RuntimeBroker.exe'}   # имена процессов (lowercase)
ignore_pids = {1, 2}                                  # PIDs, которые нужно игнорировать
ignore_cmdline_patterns = [                           # regex для cmdline
    re.compile(r'.*/docker.*'),
    re.compile(r'.*--some-flag.*'),
]

def is_ignored(info):
    """
    info: p.info из psutil.process_iter(attrs=[...])
    Возвращает True, если процесс нужно игнорировать.
    """
    name = (info.get('name') or '').lower()
    pid = info.get('pid')
    cmdline = info.get('cmdline') or []

    # 1) По pid
    if pid in ignore_pids:
        return True

    # 2) По имени (полное совпадение, нечувствительно к регистру)
    if name in ignore_names:
        return True

    # 3) По командной строке (объединяем list -> строка)
    cmd = ' '.join(cmdline) if isinstance(cmdline, (list, tuple)) else str(cmdline)
    for pattern in ignore_cmdline_patterns:
        if pattern.search(cmd):
            return True

    return False

def _key(info):
    return (info['pid'], info.get('create_time'))

# Инициализация known с учётом игнор-листа
known = set()
for p in psutil.process_iter(attrs=['pid', 'name', 'create_time', 'cmdline']):
    info = p.info
    if is_ignored(info):
        continue
    known.add(_key(info))

try:
    while True:
        current = {}
        for p in psutil.process_iter(attrs=['pid', 'name', 'create_time', 'cmdline']):
            info = p.info
            if is_ignored(info):
                continue
            current[_key(info)] = info.get('name')

        new_keys = set(current) - known
        for key in new_keys:
            pid, ctime = key
            name = current[key]
            print(f"Обнаружен новый процесс: pid={pid}, name={name}, create_time={ctime}")
            try:
                proc = psutil.Process(pid)
                proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass  # Процесс уже завершён или нет прав на убийство
        known = set(current)
        #time.sleep(0.1)
except KeyboardInterrupt:
    print("Остановлено пользователем")
