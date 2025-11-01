import win32gui
import win32api  # Добавляем этот импорт
import win32con
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class WindowAnimationState:
    """Хранит состояние анимации окна"""
    is_enabled: bool
    animation_speed: int

class WindowAnimator:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.is_reverse_x = False
        self.is_reverse_y = False
        
        # Получаем размеры экрана через win32api
        screen_width = win32api.GetSystemMetrics(0)  # SM_CXSCREEN
        screen_height = win32api.GetSystemMetrics(1)  # SM_CYSCREEN
        
        # Получаем размеры окна
        hwnd = win32gui.GetForegroundWindow()
        rect = win32gui.GetWindowRect(hwnd)
        window_width = rect[2] - rect[0]
        window_height = rect[3] - rect[1]
        
        # Устанавливаем границы движения
        self.max_x = screen_width - window_width
        self.max_y = screen_height - window_height
    
    def move_window_with_animation(self, hwnd: int, x: int, y: int):
        """
        Перемещает окно с временным отключением анимаций
        
        Args:
            hwnd: Handle окна
            x: Новая координата X
            y: Новая координата Y
        """
        try:
            
            # Получаем размеры окна
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            win32gui.MoveWindow(hwnd, x, y, width, height, True)
            
        except Exception:
                pass

    def animate(self):
        """Основной цикл анимации"""
        hwnd = win32gui.GetForegroundWindow()
        
        # Обновляем координаты X
        if not self.is_reverse_x:
            if self.x < self.max_x:
                self.x += 1
            else:
                self.is_reverse_x = True
        else:
            if self.x > 0:
                self.x -= 1
            else:
                self.is_reverse_x = False
        
        # Обновляем координаты Y
        if not self.is_reverse_y:
            if self.y < self.max_y:
                self.y += 1
            else:
                self.is_reverse_y = True
        else:
            if self.y > 0:
                self.y -= 1
            else:
                self.is_reverse_y = False
                
        self.move_window_with_animation(hwnd, self.x, self.y)
        time.sleep(0.001)

def main():
    animator = WindowAnimator()
    try:
        while True:
            animator.animate()
    except KeyboardInterrupt:
        print("\nАнимация завершена")

main()