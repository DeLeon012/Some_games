from window import *
from algorithm.functions import *
from algorithm.mouse import move, print_time
import time
from threading import Thread

moves = []
time_start_mouse = time.time()


@window.event
def on_mouse_press(*args):
    opened, game_over = mouse_press(*args)
    Map.update(opened, game_over)


@window.event
def on_draw():
    global moves
    global time_start_mouse
    main_draw()
    time_now = time.time()
    if moves and time_now >= time_start_mouse:
        first_move = moves[0]
        moves.pop(0)
        # if (check_around(first_move[0], first_move[1], Map.map)[0] and first_move[2] == 1) or first_move[2] == 4:
        task_mouse = Thread(target=move, args=[first_move[0], first_move[1], first_move[2], window, PIXELS_CELL])
        task_mouse.start()

        time_start_mouse = time_now + 0.6

    if not Map.game_over and not moves:
        moves += Map.send_moves()
        moves.sort(key=lambda x: x[2], reverse=True)


Map = Map(HEIGHT, WIDTH, numbers, PIXELS_CELL)
# print_time('Start')
pyglet.app.run(1 / 24)
