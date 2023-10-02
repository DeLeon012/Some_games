import keyboard
import time
from random import randint
import pyglet
from pyglet.window import key

SIZE_X, SIZE_Y = 12, 12
PIXEL_FOR_SQUARE = 20

window = pyglet.window.Window(
    width=(SIZE_X + 2) * PIXEL_FOR_SQUARE, height=(SIZE_Y + 2) * PIXEL_FOR_SQUARE
)

COLOR_WALL = (0, 250, 0)
COLOR_SNAKE_HEAD = (0, 150, 0)
COLOR_SNAKE_TAIL = (150, 150, 150)
COLOR_APPLE = (250, 0, 0)

PERIOD = 0.3
time_1 = time.time()


def draw_pixel_xy(x, y, color=(255, 255, 255)):
    pyglet.shapes.Rectangle(x * PIXEL_FOR_SQUARE, y * PIXEL_FOR_SQUARE, PIXEL_FOR_SQUARE - 3, PIXEL_FOR_SQUARE - 3,
                            color).draw()


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


def draw_walls():
    for x in range(2, SIZE_X):
        draw_pixel_xy(x, SIZE_Y, COLOR_WALL)
        draw_pixel_xy(x, 1, COLOR_WALL)
    for y in range(SIZE_Y, 0, -1):
        draw_pixel_xy(1, y, COLOR_WALL)
        draw_pixel_xy(SIZE_X, y, COLOR_WALL)


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


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        if -1 + param['dir'][1] != 0:
            change_dir(0, -1)
    if symbol == key.A:
        if -1 + param['dir'][0] != 0:
            change_dir(-1, 0)
    if symbol == key.S:
        if 1 + param['dir'][1] != 0:
            change_dir(0, 1)
    if symbol == key.D:
        if 1 + param['dir'][0] != 0:
            change_dir(1, 0)



@window.event
def on_draw():
    global time_1
    window.clear()
    draw_walls()
    for i in range(len(zone)):
        for j in range(len(zone[i])):
            if zone[i][j] == 'Q ':
                draw_pixel_xy(j + 1, SIZE_Y - i, COLOR_SNAKE_HEAD)
            elif zone[i][j] == '@ ':
                draw_pixel_xy(j + 1, SIZE_Y - i, COLOR_APPLE)
            elif '* ' in zone[i][j]:
                draw_pixel_xy(j + 1, SIZE_Y - i, COLOR_SNAKE_TAIL)
    if time.time() - time_1 >= PERIOD:
        time_1 = time.time()
        move()


if __name__ == '__main__':
    start()
    pyglet.app.run()
