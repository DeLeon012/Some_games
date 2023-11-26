import time
from random import randint, choice

import pyglet.app
from pyglet.window import Window
from pyglet.window import key
from pyglet.shapes import Rectangle
from pyglet.text import Label

# parameters
SIZE_X, SIZE_Y = 80, 45
PIXEL_FOR_SQUARE = 15
PER_SENT_GAP = 0.2

COLOR_WALL = (0, 250, 0)
COLOR_SNAKE_HEAD = (0, 150, 0)
COLOR_SNAKE_TAIL = (150, 150, 150)
COLOR_APPLE = (250, 0, 0)

PERIOD = 0.09
time_1 = time.time()


# Mathmatics __________________________
class vector:
    def __init__(self, x=0.0, y=0.0): self.x, self.y = x, y

    def __add__(self, other): return vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other): return self.x == other.x and self.y == other.y

    def __getitem__(self, item): return [self.x, self.y][item]


# _____________________________________


class Map:
    def __init__(self, x=SIZE_X, y=SIZE_Y):
        self.size_x = x
        self.size_y = y
        self.apple_position = vector(randint(3, SIZE_X), randint(3, SIZE_Y))
        self.apple_possible_positions = set(i * 1000 + j
                                            for i in range(3, SIZE_X)
                                            for j in range(3, SIZE_Y))

    def eat_apple(self):
        snake_set = set()
        snake_set.add(snake.head_position.x * 1000 + snake.head_position.y)
        for i in snake.tail:
            snake_set.add(i.x * 1000 + i.y)
        possible_positions = self.apple_possible_positions - snake_set
        xy = choice(tuple(possible_positions))
        self.apple_position = vector(xy // 1000, xy % 1000)


class Snake:
    def __init__(self):
        self.head_position = vector(randint(3, SIZE_X), randint(3, SIZE_Y))
        self.tail = list()
        self.direction = vector(0, 1)
        self.score = 0
        self.game_over = False

    def move(self):
        if self.game_over:
            return
        self.tail.append(self.head_position)
        self.head_position += self.direction
        if not (3 <= self.head_position.x <= SIZE_X and 3 <= self.head_position.y <= SIZE_Y) \
                or self.head_position in self.tail:
            self.game_over = True
        if not (Map.apple_position == self.head_position):
            self.tail.pop(0)
        else:
            self.score += 1
            Map.eat_apple()


def draw_rectangle(x_coord, y_coord, color):
    return Rectangle(x_coord * PIXEL_FOR_SQUARE, y_coord * PIXEL_FOR_SQUARE,
                     PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP), PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP), color,
                     batch=wall_batch)


snake = Snake()
Map = Map()
Window = Window(width=(Map.size_x + 4) * PIXEL_FOR_SQUARE,
                height=(Map.size_y + 4) * PIXEL_FOR_SQUARE)
wall_batch = pyglet.graphics.Batch()
wall_list = list()

for x in range(2, SIZE_X + 2):
    wall_list.append(draw_rectangle(x, 2, COLOR_WALL))
    wall_list.append(draw_rectangle(x, SIZE_Y + 1, COLOR_WALL))
for y in range(2, SIZE_Y + 2):
    wall_list.append(draw_rectangle(2, y, COLOR_WALL))
    wall_list.append(draw_rectangle(SIZE_X + 1, y, COLOR_WALL))
score = Label(f"Score: {snake.score}", font_name='Corbel', font_size=15,
              x=40, y=Window.height - 20, batch=wall_batch)


@Window.event
def on_key_press(*args):
    symbol = args[0]
    if symbol == key.W or symbol == key.UP:
        new_direction = vector(0, 1)
    elif symbol == key.S or symbol == key.DOWN:
        new_direction = vector(0, -1)
    elif symbol == key.A or symbol == key.LEFT:
        new_direction = vector(-1, 0)
    elif symbol == key.D or symbol == key.RIGHT:
        new_direction = vector(1, 0)
    else:
        return

    if snake.tail:
        if snake.tail[-1] != snake.head_position + new_direction:
            snake.direction = new_direction
    else:
        snake.direction = new_direction


@Window.event
def on_draw():
    global time_1
    Window.clear()
    score.text = f"Score: {snake.score}"
    wall_batch.draw()

    snake.move()
    draw_rectangle(*Map.apple_position, COLOR_APPLE).draw()
    draw_rectangle(*snake.head_position, COLOR_SNAKE_HEAD).draw()
    for point in snake.tail:
        draw_rectangle(*point, COLOR_SNAKE_TAIL).draw()

    if snake.game_over:
        Label("G A M E  O V E R", font_name='Corbel', font_size=20, bold=True,
              x=Window.width // 2 - 90, y=Window.height // 2).draw()


if __name__ == '__main__':
    pyglet.app.run(PERIOD)
