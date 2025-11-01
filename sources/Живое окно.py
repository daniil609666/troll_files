import pyautogui as pg
# Отключить защиту от сбоев PyAutoGUI 
pg.FAILSAFE = False 
import random
def move():
    for _ in range(3):  # Run 3 times
        pg.hotkey('winleft', 'down')
        pg.hotkey('esc')
        pg.hotkey('winleft', 'up')
        pg.hotkey('esc')
        pg.hotkey('winleft', 'down')
        pg.hotkey('esc')
        pg.hotkey('winleft', 'up')

        wait_time = random.uniform(0.5, 1)
        pg.sleep(wait_time)

        pg.hotkey('winleft', 'right')
        pg.hotkey('esc')
        pg.hotkey('winleft', 'left')
        pg.hotkey('esc')
        pg.hotkey('winleft', 'right')
        pg.hotkey('esc')
        pg.hotkey('winleft', 'left')
    wait_time = random.uniform(0.5, 1)
    pg.sleep(wait_time)

    wait_time = random.uniform(0.5, 1)
    pg.sleep(wait_time)
    move()

move()
