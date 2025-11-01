import random
import sys
import time
import pyautogui
pyautogui.FAILSAFE=False
sys.setrecursionlimit(99999999)
rand = random.choice([-1, 1])
def mouse():
    randx = random.choice([-10, 10])
    randy = random.choice([-10, 10])
    pyautogui.move(randx, randy)
    mouse()
mouse()