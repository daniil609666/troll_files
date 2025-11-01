import pyautogui
pyautogui.FAILSAFE= False
def rep():
    pyautogui.scroll(100)
    pyautogui.scroll(-100)
    rep()
rep()