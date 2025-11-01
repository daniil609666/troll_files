import ctypes

def is_safe_mode():
    """Проверяет, работает ли Windows в безопасном режиме, используя GetSystemMetrics."""
    # SM_CLEANBOOT = 67
    # 0 - Normal boot
    # 1 - Safe Mode
    # 2 - Safe Mode with network
    # 3 - Safe Mode with command prompt
    return ctypes.windll.user32.GetSystemMetrics(67) != 0


if __name__ == "__main__":
    if is_safe_mode():
        print("Windows работает в безопасном режиме.")
    else:
        print("Windows не работает в безопасном режиме.")