import pyautogui, time, random
pyautogui.FAILSAFE = False
while True:
    rand = ['restore', 'close']
    rand = random.choice(rand)
    rand_time = random.randint(1, 10)
    print(f'жду {rand_time}, затем делаю {rand}')
    time.sleep(rand_time)
    if rand == 'close':
        pyautogui.hotkey('ctrl', 'w')
    else:
        pyautogui.hotkey('ctrl', 'shift', 't')
    