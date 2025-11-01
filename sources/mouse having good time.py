import win32api
import win32con
import time
import random

def bounce_cursor(delay=0.01, speed=10):
    """
    Moves the cursor around the screen, bouncing off the edges.

    Args:
        delay (float): Time in seconds between cursor movements.  Smaller = faster.
        speed (int):  How many pixels the cursor moves per step.  Larger = faster.
    """
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)

    dx = random.choice([-speed, speed])  # Initial X direction
    dy = random.choice([-speed, speed])  # Initial Y direction

    while True:
        x += dx
        y += dy

        # Bounce off left/right edges
        if x < 0:
            x = 0
            dx = speed  # Reverse X direction
        elif x > screen_width - 1:
            x = screen_width - 1
            dx = -speed  # Reverse X direction

        # Bounce off top/bottom edges
        if y < 0:
            y = 0
            dy = speed  # Reverse Y direction
        elif y > screen_height - 1:
            y = screen_height - 1
            dy = -speed  # Reverse Y direction

        win32api.SetCursorPos((x, y))
        time.sleep(delay)


while True:
    try:
        bounce_cursor(delay=0.01, speed=10)  # Start the bouncing effect
    except:
        pass