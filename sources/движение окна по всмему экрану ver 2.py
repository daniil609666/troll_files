import win32gui
import win32api  
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
    def __init__(self, target_window_title: str):
        """
        Инициализирует аниматор окна
        
        Args:
            target_window_title: Заголовок окна, которое нужно анимировать
        """
        self.target_window_title = target_window_title
        self.x = 0
        self.y = 0
        self.is_reverse_x = False
        self.is_reverse_y = False
        
        # Получаем размеры экрана через win32api
        screen_width = win32api.GetSystemMetrics(0)  # SM_CXSCREEN
        screen_height = win32api.GetSystemMetrics(1)  # SM_CYSCREEN
        
        # Получаем размеры экрана для установки границ
        self.max_x = screen_width
        self.max_y = screen_height
    
    def get_target_window_handle(self) -> Optional[int]:
        """
        Находит handle окна по заголовку
        
        Returns:
            Handle окна или None если окно не найдено
        """
        def win_enum_handler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if window_text == self.target_window_title:
                    ctx.append(hwnd)
                    
        windows = []
        win32gui.EnumWindows(win_enum_handler, windows)
        return windows[0] if windows else None

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
        hwnd = self.get_target_window_handle()
        
        if not hwnd:
            print(f"Окно с заголовком '{self.target_window_title}' не найдено")
            time.sleep(1)  # Ждем перед повторной попыткой
            return
            
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
    window_title ="Заголовок окна"
    animator = WindowAnimator(window_title)
    try:
        while True:
            animator.animate()
    except KeyboardInterrupt:
        print("\nАнимация завершена")

main()