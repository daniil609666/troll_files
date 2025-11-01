import win32api, win32gui, random, win32con, time
desk = win32gui.GetDC(0)
xx = win32api.GetSystemMetrics(0)
yy = win32api.GetSystemMetrics(1)
while True:
    msgs = ['RIP PC!', 'BY DAN609', 'Ты не сможешь меня удалить!', 'BAN!', 'You cant delete me!']
    text = random.choice(msgs)
    win32gui.DrawText(desk, text, len(text), (random.randrange(xx), random.randrange(yy), random.randrange(xx), random.randrange(yy)), win32con.DT_LEFT)
    time.sleep(00.1)