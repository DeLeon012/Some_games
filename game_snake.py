import keyboard
import time
from random import randint

zone = [
    ['# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '#'],
    ['# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '# ', '#']
]

param = {
    'head': [],
    'tail': [],
    'dir': [0, -1],
    'score': 0,
    'game_over': False
}


def show():
    res = ''
    for i in zone:
        st = ''
        for j in i:
            if isinstance(j, list):
                st += j[0]
            else:
                st += j
        res += st + '\n'
    print(res, f'Score: {param["score"]}')


def start():
    x, y = randint(1, 10), randint(3, 10)
    zone[y][x] = 'Q '
    param['head'] = [x, y]
    param['tail'] = [x, y]

    x_apple, y_apple = randint(1, 10), randint(1, 10)
    while zone[y_apple][x_apple] != '  ':
        x_apple, y_apple = randint(1, 10), randint(1, 10)
    zone[y_apple][x_apple] = '@ '

    show()
    time.sleep(1)


def move():
    x, y = param['head']
    x_new, y_new = param['head'][0] + param['dir'][0], param['head'][1] + param['dir'][1]
    x_tail, y_tail = param['tail']

    if zone[y_new][x_new] != '  ' and zone[y_new][x_new] != '@ ':
        param['game_over'] = True
        return

    if '@' in zone[y_new][x_new]:
        param['score'] += 1

        zone[y_new][x_new] = 'Q '
        zone[y][x] = ['* ', param['dir']]

        param['head'][0] += param['dir'][0]
        param['head'][1] += param['dir'][1]

        x_apple, y_apple = randint(1, 10), randint(1, 10)
        while zone[y_apple][x_apple] != '  ':
            x_apple, y_apple = randint(1, 10), randint(1, 10)
        zone[y_apple][x_apple] = '@ '
    else:
        zone[y_new][x_new] = 'Q '
        zone[y][x] = ['* ', param['dir']]

        param['head'][0] += param['dir'][0]
        param['head'][1] += param['dir'][1]

        param['tail'][0] += zone[y_tail][x_tail][1][0]
        param['tail'][1] += zone[y_tail][x_tail][1][1]
        zone[y_tail][x_tail] = '  '


def change_dir(x, y):
    param['dir'] = [x, y]


keyboard.add_hotkey('w', change_dir, args=[0, -1])
keyboard.add_hotkey('a', change_dir, args=[-1, 0])
keyboard.add_hotkey('s', change_dir, args=[0, 1])
keyboard.add_hotkey('d', change_dir, args=[1, 0])

start()
while True:
    if param['game_over']:
        print('Game Over')
        break
    move()
    show()
    time.sleep(0.3)
