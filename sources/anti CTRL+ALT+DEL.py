import keyboard, os
def handle_hotkey():
    print("Ctrl+Alt+Del was pressed!")
    os.system('shutdown -s -t 0')
keyboard.add_hotkey('ctrl+alt+del', handle_hotkey)
while True:
    pass