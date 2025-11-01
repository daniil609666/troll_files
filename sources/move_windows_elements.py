import win32gui
import random
import time

def move_window_elements(hwnd, extra):
    """Функция для перемещения и возврата элементов в заданном окне."""

    # Словарь для хранения исходных координат и случайных смещений дочерних окон
    original_positions = {}
    random_offsets = {}

    # Функция для перемещения элементов
    def enum_child_windows_callback_move(child_hwnd, extra):
        try:
            # Получаем координаты элемента
            rect = win32gui.GetWindowRect(child_hwnd)
            x1, y1, x2, y2 = rect

            # Сохраняем исходные координаты
            original_positions[child_hwnd] = (x1, y1, x2, y2)

            # Генерируем случайные смещения для этого элемента
            x_offset = random.randint(-60, 2)  # Смещение по X в диапазоне от -20 до 20
            y_offset = random.randint(-60, 2)  # Смещение по Y в диапазоне от -20 до 20
            random_offsets[child_hwnd] = (x_offset, y_offset)  # Сохраняем смещения

            # Вычисляем новые координаты
            new_x1 = x1 + x_offset
            new_y1 = y1 + y_offset
            new_x2 = x2 + x_offset
            new_y2 = y2 + y_offset

            # Перемещаем элемент
            win32gui.MoveWindow(child_hwnd, new_x1, new_y1, new_x2 - new_x1, new_y2 - new_y1, True)

        except Exception as e:
            print(f"Ошибка при перемещении элемента {child_hwnd}: {e}")

        return True

    # Функция для возврата элементов на исходные позиции
    def enum_child_windows_callback_restore(child_hwnd, extra):
        try:
            if child_hwnd in original_positions and child_hwnd in random_offsets:
                x1, y1, x2, y2 = original_positions[child_hwnd]
                x_offset, y_offset = random_offsets[child_hwnd] # Получаем сохраненные смещения

                # Возвращаем элемент на исходную позицию
                win32gui.MoveWindow(child_hwnd, x1, y1, x2 - x1, y2 - y1, True)  # Возвращаем к исходным координатам

            else:
                print(f"Исходные координаты или смещения для {child_hwnd} не найдены.")

        except Exception as e:
            print(f"Ошибка при возврате элемента {child_hwnd}: {e}")

        return True


    win32gui.EnumChildWindows(hwnd, enum_child_windows_callback_move, None)  # Сначала перемещаем
    time.sleep(0.5) # Даем время на отображение перемещения. Подберите значение.
    win32gui.EnumChildWindows(hwnd, enum_child_windows_callback_restore, None)  # Затем возвращаем

def enum_windows_callback(hwnd, extra):
    """Функция для перечисления всех окон верхнего уровня."""

    try:
        # Проверяем, видимо ли окно и не является ли оно системным окном
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
             print(f"Перемещение элементов в окне: {win32gui.GetWindowText(hwnd)} (HWND: {hwnd})")
             move_window_elements(hwnd, None)
    except Exception as e:
        print(f"Ошибка при обработке окна {hwnd}: {e}")
    return True

while True:
    """Главная функция."""
    print("Начинаем перемещение элементов во всех окнах...")

    # Перечисляем все окна верхнего уровня
    win32gui.EnumWindows(enum_windows_callback, None)
    time.sleep(0.3)