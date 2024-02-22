import pyglet.graphics
from pyglet.window import key
from pyglet.text import Label
from pyglet.image.codecs.pil import PILImageDecoder
from time import time

from classes import *

# Parameters
A_FRICTION = 0.08
CAR_ROTATE = 0.25
F_CAR = 1
SCALE = 0.8
CAR_ROTATE_WHEEL = -5

window = pyglet.window.Window(
    fullscreen=True
)
pyglet.gl.glClearColor(0.6, 0.6, 0.6, 1)

map_points = [
    vector(39, 323), vector(36, 525), vector(112, 727), vector(254, 853), vector(563, 875), vector(1054, 850),
    vector(1114, 773), vector(1076, 709), vector(734, 615), vector(545, 553), vector(816, 564), vector(1106, 647),
    vector(1250, 711), vector(1452, 700), vector(1501, 510), vector(1426, 311), vector(1116, 266), vector(559, 262),
    vector(214, 244), vector(40, 324)
]

map_points_2 = [
    vector(150, 428), vector(148, 594), vector(237, 734), vector(426, 770), vector(706, 782), vector(860, 780),
    vector(947, 767), vector(949, 762), vector(799, 714), vector(571, 642), vector(533, 618), vector(414, 552),
    vector(402, 470), vector(404, 464), vector(492, 414), vector(762, 462), vector(943, 507), vector(1108, 549),
    vector(1272, 605), vector(1348, 575), vector(1346, 490), vector(1234, 401), vector(966, 370), vector(442, 355),
    vector(150, 429)
]

finish_line = [vector(36, 474), vector(149, 474)]
checkpoint_line = [vector(1347, 575), vector(1477, 604)]

player = Player()
time_start = time()

car = Car(SCALE)
image_car = pyglet.image.load('sports-car-delorean', file=car_image, decoder=PILImageDecoder())
image_car.anchor_x = 130
image_car.anchor_y = 20

image_map = pyglet.image.load(filename='Map_image', file=map_image, decoder=PILImageDecoder())
Sprite_map = pyglet.sprite.Sprite(image_map, -150, 0)


def new_batch():
    labels_batch = pyglet.graphics.Batch()
    for i in range(len(player.laps)):
        print(i)
        Label(f'Lap {i + 1}: {int(player.laps[i] // 60)} мин {int(player.laps[i] % 60)}'
              f' сек {int(player.laps[i] * 100 % 100)}', font_name='Bahnschrift', font_size=12,
              x=window.width - 300, y=(window.height - 50) - 18 * (len(player.laps) - i), batch=labels_batch).draw()
    labels_batch.draw()
    return labels_batch


scores_text = ''


@window.event
def on_key_press(*args):
    symbol = args[0]
    if symbol == key.W or symbol == key.UP:
        car.F += F_CAR
    if symbol == key.S or symbol == key.DOWN:
        car.F += -F_CAR * 0.4
    elif symbol == key.A or symbol == key.LEFT:
        car.rotate += CAR_ROTATE
    elif symbol == key.D or symbol == key.RIGHT:
        car.rotate += -CAR_ROTATE


@window.event
def on_key_release(*args):
    symbol = args[0]
    if symbol == key.W or symbol == key.UP:
        car.F -= F_CAR
    if symbol == key.S or symbol == key.DOWN:
        car.F -= -F_CAR * 0.4
    elif symbol == key.A or symbol == key.LEFT:
        car.rotate -= CAR_ROTATE
    elif symbol == key.D or symbol == key.RIGHT:
        car.rotate -= -CAR_ROTATE

    elif symbol == key.Q:
        player.checkpoint = (player.checkpoint + 1) % 2


@window.event
def on_draw():
    global time_start, scores_text
    window.clear()

    Sprite_map.draw()
    car.move(A_FRICTION)
    car.draw_car(image_car, CAR_ROTATE_WHEEL)

    for i in range(len(map_points) - 1):
        if any(check_cross_lines(*j, map_points[i], map_points[i + 1]) for j in car.lines()):
            car.restart()
            player.count_of_dies += 1
            player.checkpoint = False

    for i in range(len(map_points_2) - 1):
        if any(check_cross_lines(*j, map_points_2[i], map_points_2[i + 1]) for j in car.lines()):
            car.restart()
            player.count_of_dies += 1
            player.checkpoint = False

    time_end = time()

    if any(check_cross_lines(*j, *finish_line) for j in car.lines()) and player.checkpoint:
        player.laps.append(time_end - time_start)
        scores_text = f'Lap {len(player.laps)}: {int((time_end - time_start) // 60)}:' \
                      f'{int((time_end - time_start) % 60)}.{int((time_end - time_start) * 100 % 100)}\n' + scores_text
        player.checkpoint = False
        time_start = time_end

    elif any(check_cross_lines(*j, *checkpoint_line) for j in car.lines()) and not player.checkpoint:
        player.checkpoint = True

    Label('Управление: WASD или стрелками\nEsc - закрыть игру', font_name='Corbel', font_size=10, x=15, y=30,
          multiline=True, width=300).draw()

    Label(scores_text, font_name='Bahnschrift', font_size=12,
          x=window.width - 300, y=window.height - 50 - 18, multiline=True, width=250).draw()

    Label(f'Lap {len(player.laps) + 1}: {int((time_end - time_start) // 60)}:{int((time_end - time_start) % 60)}.'
          f'{int((time_end - time_start) * 100 % 100)}', font_name='Bahnschrift', font_size=12,
          x=window.width - 300, y=window.height - 50).draw()

    Label(f'Count of crashes: {player.count_of_dies}', font_name='Bahnschrift', font_size=12,
          x=150, y=window.height - 50).draw()


pyglet.app.run()
