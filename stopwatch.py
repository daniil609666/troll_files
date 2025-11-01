
from time import sleep

def sec():
    try:
        with open('time.txt', 'r', encoding='utf-8') as backup:
            data = backup.read().strip()
            numbers = [int(s) for s in data.split() if s.isdigit()]
            if len(numbers) == 3:
                count_hours, count_minutes, count = numbers
            else:
                count_hours = count_minutes = count = 0
    except FileNotFoundError:
        count_hours = count_minutes = count = 0

    while True:
        print(f'Прошло часов:{count_hours}, Прошло минут:{count_minutes}, Прошло секунд:{count}')
        with open('time.txt', 'w', encoding='utf-8') as f:
            f.write(f'{count_hours} {count_minutes} {count}')

        count += 1
        if count == 60:
            count = 0
            count_minutes += 1
        if count_minutes == 60:
            count_minutes = 0
            count_hours += 1

        sleep(1)

sec()
