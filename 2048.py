import json
import time
import keyboard
from random import randrange

SIZE = 4
WIDTH = 6
SPAWN = [2] * 9 + [4]
status = {
    'game_over': False, 'victory': False, 'show': False, 'score': 0, 'best_score': 0
}

try:
    with open('2048_best_score.json') as f:
        status['best_score'] = json.load(f)
except:
    status['best_score'] = 0

table = []
for _ in range(SIZE):
    ll = []
    for _ in range(SIZE):
        ll.append('')
    table.append(ll)


def show():
    res = '_' * WIDTH * SIZE + '\n' + ' ' * WIDTH * SIZE + '|' + '\n'
    for i in table:
        st = ''
        for j in i:
            right = (WIDTH - len(j)) // 2
            left = right + len(j) % 2
            st += ' ' * left + j + ' ' * right
        res += st + '|' + '\n'
        res += ' ' * WIDTH * SIZE + '|' + '\n'
    res = res[:-(WIDTH * SIZE + 2)] + '_' * WIDTH * SIZE + '|' + '\n'
    print(res, f"Score: {status['score']}")

    if status['game_over']:
        ind = len(res) // 2 + WIDTH * SIZE // 2 - (WIDTH * SIZE + 2)
        res = res[:ind - 10] + ' G A M E  O V E R ( ' + res[ind + 10:]
        print(res)
        save_result()
    elif status['victory'] and not status['show']:
        ind = len(res) // 2 + WIDTH * SIZE // 2 - (WIDTH * SIZE + 2)
        res = res[:ind - 8] + ' V I C T O R Y )' + res[ind + 8:]
        print(res)
        status['show'] = True
        time.sleep(3)
        show()


def save_result():
    status['best_score'] = max(status['best_score'], status['score'])
    with open('2048_best_score.json', 'w') as file:
        json.dump(status['best_score'], file)
    print(f"Score: {status['score']} \nBest Score: {status['best_score']}")


def spawn():
    new = SPAWN[randrange(len(SPAWN))]
    if not have_empty():
        return
    while True:
        x, y = randrange(SIZE), randrange(SIZE)
        if table[y][x] == '':
            table[y][x] = str(new)
            break


def move_up_down(arg1, arg2):
    flag = []
    for x in range(SIZE):
        line = []
        for y in range(*arg1):
            line.append(table[y][x])
        new_line = rebuild(line)
        flag.append(new_line)
        if new_line:
            new_line = new_line[::arg2]
            for y2 in range(SIZE):
                table[y2][x] = new_line[y2]
    if any(flag):
        return True
    else:
        return False


def move_left_right(arg1, arg2):
    flag = []
    for y in range(SIZE):
        line = []
        for x in range(*arg1):
            line.append(table[y][x])
        new_line = rebuild(line)
        flag.append(new_line)
        if new_line:
            new_line = new_line[::arg2]
            for x2 in range(SIZE):
                table[y][x2] = new_line[x2]
    if any(flag):
        return True
    else:
        return False


def move(num, arg1, arg2):
    if num:
        flag = move_up_down(arg1, arg2)
    else:
        flag = move_left_right(arg1, arg2)

    if check_game_over():
        status['game_over'] = True
        show()
    elif flag:
        spawn()
        show()
# def generate(arr):
#     old = arr.copy()
#     for i in range(len(arr) - 1):
#         for j in range(i + 1, len(arr)):
#             if not arr[j]:
#                 continue
#             elif arr[i] == arr[j]:
#                 arr[i] = str(int(arr[i]) * 2)
#                 arr[j] = ''
#             else:
#                 if arr[i]:
#                     arr[i + 1] = arr[j]
#                     if j - i != 1:
#                         arr[j] = ''
#                 else:
#                     arr[i] = arr[j]
#                     arr[j] = ''
#             break
#     if old == arr:
#         return False
#     return arr


def rebuild(arr: list):
    old = arr.copy()
    try:
        while True:
            arr.remove('')
    except:
        i = 0
        while i < len(arr) - 1:
            if arr[i] == arr[i + 1]:
                arr[i] = str(int(arr[i]) * 2)
                arr.pop(i + 1)
                status['score'] += int(arr[i])
            i += 1
        arr += [''] * (SIZE - len(arr))
    if '2048' in arr:
        status['victory'] = True
    if old == arr:
        return False
    return arr


def have_empty():
    for x in table:
        for j in x:
            if not j:
                return True
    return False


def check_game_over():
    if have_empty():
        return False
    for y in range(SIZE - 1):
        for x in range(SIZE):
            if table[y][x] == table[y + 1][x]:
                return False
    for y in range(SIZE):
        for x in range(SIZE - 1):
            if table[y][x] == table[y][x + 1]:
                return False
    return True


keyboard.add_hotkey('up', move, args=[1, [SIZE], 1])
keyboard.add_hotkey('down', move, args=[1, [SIZE - 1, -1, -1], -1])
keyboard.add_hotkey('left', move, args=[0, [SIZE], 1])
keyboard.add_hotkey('right', move, args=[0, [SIZE - 1, -1, -1], -1])

spawn()
spawn()
show()

while not status['game_over']:
    time.sleep(1)
