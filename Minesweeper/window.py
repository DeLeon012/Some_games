import pyglet
from pyglet.shapes import Line
from pyglet.sprite import Sprite
from pyglet.text import Label
from random import randint
from pyglet.image.codecs.pil import PILImageDecoder
from texture import *

HEIGHT, WIDTH = 20, 40
PIXELS_CELL = 34
LINE_WIDTH = 2
PER_SENT_BOMBS = 14  # %
GAME_OVER = False
number_colors = {
    1: (0, 0, 255, 255), 2: (0, 128, 0, 255), 3: (255, 0, 0, 255), 4: (0, 0, 128, 255), 5: (128, 0, 0, 255),
    6: (0, 128, 128, 255), 7: (128, 0, 128, 255), 8: (0, 0, 0, 255)
}
window = pyglet.window.Window(height=HEIGHT * PIXELS_CELL + 50, width=WIDTH * PIXELS_CELL)

pyglet.gl.glClearColor(0.776, 0.776, 0.776, 0)

cell_img = pyglet.image.load('cell', file=cell_image, decoder=PILImageDecoder())
cell_img.anchor_x, cell_img.anchor_y = 1, -1

cell_flag_img = pyglet.image.load('cell_flag', file=cell_flag_image, decoder=PILImageDecoder())
cell_flag_img.anchor_x, cell_flag_img.anchor_y = 1, -1

bomb_img = pyglet.image.load('bomb', file=bomb_image, decoder=PILImageDecoder())
bomb_img.anchor_x, bomb_img.anchor_y = -1, -1

cells_set = dict()
cells_flag_set = set()
bombs_set = set()
last_opened = set()
# count_moves = -1

numbers = {
    1: set(), 2: set(), 3: set(),
    4: set(), 5: set(), 6: set(), 7: set(), 8: set()}
statistic = {
    'count_bombs': 0,
    'count_flags': 0}
for i in range(0, WIDTH * PIXELS_CELL, PIXELS_CELL):
    for j in range(0, HEIGHT * PIXELS_CELL, PIXELS_CELL):
        if randint(0, 100) < PER_SENT_BOMBS:
            bombs_set.add(i * 1000 + j)
            statistic['count_bombs'] += 1

cell_batch = pyglet.graphics.Batch()
for i in range(0, WIDTH * PIXELS_CELL, PIXELS_CELL):
    for j in range(0, HEIGHT * PIXELS_CELL, PIXELS_CELL):
        n = i * 1000 + j
        cells_set[n] = Sprite(cell_img, i, j, batch=cell_batch)

        if n not in bombs_set:
            count = 0
            for d_x in (-PIXELS_CELL, 0, PIXELS_CELL):
                for d_y in (-PIXELS_CELL, 0, PIXELS_CELL):
                    if ((i + d_x) * 1000 + (j + d_y)) in bombs_set:
                        count += 1
            if count != 0:
                numbers[count].add(n)

empty_cells = set()
for i in range(0, WIDTH * PIXELS_CELL, PIXELS_CELL):
    for j in range(0, HEIGHT * PIXELS_CELL, PIXELS_CELL):
        n = i * 1000 + j
        if n not in bombs_set and not any(n in sets for sets in numbers.values()):
            empty_cells.add(n)

number_batch = pyglet.graphics.Batch()
number_list = []
for number in range(1, 9):
    for cell in numbers[number]:
        number_list.append(
            Label(str(number), font_name='Bahnschrift', font_size=PIXELS_CELL * 0.65,
                  x=cell // 1000 + PIXELS_CELL * 0.25, y=cell % 1000 + PIXELS_CELL * 0.25,
                  color=number_colors[number], batch=number_batch)
        )

lines_batch = pyglet.graphics.Batch()
lines_list = []
for i in range(0, WIDTH * PIXELS_CELL, PIXELS_CELL):
    lines_list.append(Line(i, 0, i, HEIGHT * PIXELS_CELL, width=LINE_WIDTH, color=(128, 128, 128), batch=lines_batch))
for i in range(0, HEIGHT * PIXELS_CELL, PIXELS_CELL):
    lines_list.append(Line(0, i, WIDTH * PIXELS_CELL, i, width=LINE_WIDTH, color=(128, 128, 128), batch=lines_batch))


def dict_pop(dictionary, key):
    try:
        del dictionary[key]
        last_opened.add(key)
    except KeyError:
        pass


def clear_spaces(xy, already=None, direction=0):
    if not already:
        already = set()
    if xy in already or not (0 <= xy // 1000 <= WIDTH * PIXELS_CELL - PIXELS_CELL) \
            or not (0 <= xy % 1000 <= HEIGHT * PIXELS_CELL - PIXELS_CELL):
        return
    dict_pop(cells_set, xy)
    already.add(xy)
    if xy not in empty_cells:
        dict_pop(cells_set, xy + direction)
        if xy + direction in empty_cells:
            clear_spaces(xy + direction, already)
        dict_pop(cells_set, xy - direction)
        if xy - direction in empty_cells:
            clear_spaces(xy - direction, already)
        return
    clear_spaces(xy + PIXELS_CELL, already, -PIXELS_CELL * 1000)
    clear_spaces(xy + PIXELS_CELL * 1000, already, PIXELS_CELL)
    clear_spaces(xy - PIXELS_CELL, already, PIXELS_CELL * 1000)
    clear_spaces(xy - PIXELS_CELL * 1000, already, -PIXELS_CELL)


def click_on_cell(xy):
    global GAME_OVER
    if xy in empty_cells:
        clear_spaces(xy)
    elif xy in cells_flag_set:
        return
    elif xy in bombs_set:
        GAME_OVER = True
        for k in bombs_set:
            dict_pop(cells_set, k)
            cells_flag_set.discard(k)
    else:
        dict_pop(cells_set, xy)


interface = pyglet.graphics.Batch()
interface_bomb_image = Sprite(bomb_img, 20, HEIGHT * PIXELS_CELL + 12, batch=interface)
interface_bomb_count = Label(': ' + str(statistic['count_bombs']), font_name='Bahnschrift',
                             font_size=PIXELS_CELL * 0.65,
                             x=60, y=HEIGHT * PIXELS_CELL + 20, color=(0, 0, 0, 255), batch=interface)

interface_flag_image = Sprite(cell_flag_img, 150, HEIGHT * PIXELS_CELL + 12, batch=interface)
interface_flag_count = Label(': ' + str(statistic['count_flags']), font_name='Bahnschrift',
                             font_size=PIXELS_CELL * 0.65,
                             x=190, y=HEIGHT * PIXELS_CELL + 20, color=(0, 0, 0, 255),
                             batch=interface)


# instructions = Label("Левая кнопка мыши - открыть клетку \nПравая кнопка мыши - поставить / убрать флаг",
#                      font_name='Bahnschrift', font_size=PIXELS_CELL * 0.3, multiline=True, width=300,
#                      anchor_y='center',
#                      x=WIDTH * PIXELS_CELL - 300, y=HEIGHT * PIXELS_CELL + 25, color=(0, 0, 0, 255),
#                      batch=interface)


def mouse_press(*args):
    global GAME_OVER
    last_opened.clear()

    x, y, button = args[:3]
    x -= x % PIXELS_CELL
    y -= y % PIXELS_CELL
    xy = x * 1000 + y
    if button == 1 and xy not in cells_flag_set:
        dict_pop(cells_set, xy)
        if xy in bombs_set:
            GAME_OVER = True
            for k in bombs_set:
                dict_pop(cells_set, k)
                cells_flag_set.discard(k)
        elif xy in empty_cells:
            clear_spaces(xy)
        else:
            num = find_number(numbers, xy)
            count_flags = 0
            for f_x in (-PIXELS_CELL, 0, PIXELS_CELL):
                for f_y in (-PIXELS_CELL, 0, PIXELS_CELL):
                    f_xy = (f_x + x) * 1000 + (f_y + y)
                    if f_xy in cells_flag_set:
                        count_flags += 1
            if num == count_flags:
                for f_x in (-PIXELS_CELL, 0, PIXELS_CELL):
                    for f_y in (-PIXELS_CELL, 0, PIXELS_CELL):
                        f_xy = (f_x + x) * 1000 + (f_y + y)
                        click_on_cell(f_xy)

    elif button == 4:
        if xy in cells_set:
            del cells_set[xy]
            cells_flag_set.add(xy)
            statistic['count_flags'] += 1
        elif xy in cells_flag_set:
            cells_set[xy] = Sprite(cell_img, xy // 1000, xy % 1000, batch=cell_batch)
            cells_flag_set.discard(xy)
            statistic['count_flags'] -= 1

    return last_opened, GAME_OVER


def main_draw():
    window.clear()
    lines_batch.draw()
    number_batch.draw()
    cell_batch.draw()

    for flag in cells_flag_set:
        cell_flag_img.blit(flag // 1000, flag % 1000)
    if GAME_OVER:
        for bomb in bombs_set:
            Sprite(bomb_img, bomb // 1000, bomb % 1000).draw()
        Label("G A M E  O V E R", font_name='Bahnschrift', font_size=PIXELS_CELL * 1.25, anchor_x='center',
              x=WIDTH * PIXELS_CELL // 2, y=HEIGHT * PIXELS_CELL // 2, color=(0, 0, 0, 255)).draw()
        Label("G A M E  O V E R", font_name='Bahnschrift', font_size=PIXELS_CELL * 1.2, anchor_x='center',
              x=WIDTH * PIXELS_CELL // 2, y=HEIGHT * PIXELS_CELL // 2, color=(138, 127, 142, 255)).draw()

    interface_flag_count.text = ': ' + str(statistic['count_flags'])
    interface.draw()
