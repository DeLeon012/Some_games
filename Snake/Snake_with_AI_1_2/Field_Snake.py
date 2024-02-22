from my_math.decart_vecor import vector
from my_math.Linked_list import LinkedList
from configs import *

from random import randint

import pyglet.app
from pyglet.window import Window, key
from pyglet.shapes import Rectangle
from pyglet.shapes import Line
from pyglet.text import Label


class Map:
    def __init__(self, x=SIZE_X, y=SIZE_Y):
        self.window = Window(width=SIZE_X * PIXEL_FOR_SQUARE,
                             height=SIZE_Y * PIXEL_FOR_SQUARE)

        self.size_x = x
        self.size_y = y
        self.apple_position = vector(randint(WALLS_GAP + 1, SIZE_X - WALLS_GAP - 1),
                                     randint(WALLS_GAP + 1, SIZE_Y - WALLS_GAP - 1))
        self.apple_possible_positions = set(i * 1000 + j
                                            for i in range(WALLS_GAP + 1, SIZE_X - WALLS_GAP)
                                            for j in range(WALLS_GAP + 1, SIZE_Y - WALLS_GAP))

        self.wall_batch = pyglet.graphics.Batch()

        points = [i * PIXEL_FOR_SQUARE for i in
                  [vector(WALLS_GAP + 0.4 - 1 / WALL_WIDTH, WALLS_GAP + 0.4 - 1 / WALL_WIDTH),
                   vector(WALLS_GAP + 0.4 - 1 / WALL_WIDTH, SIZE_Y - WALLS_GAP - 0.4 + 1 / WALL_WIDTH),
                   vector(SIZE_X - WALLS_GAP - 0.4 + 1 / WALL_WIDTH, WALLS_GAP + 0.4 - 1 / WALL_WIDTH),
                   vector(SIZE_X - WALLS_GAP - 0.4 + 1 / WALL_WIDTH, SIZE_Y - WALLS_GAP - 0.4 + 1 / WALL_WIDTH)]
                  ]

        self.wall_list = [
            Line(*points[0], *points[1], color=COLOR_WALL, batch=self.wall_batch, width=WALL_WIDTH),
            Line(*points[0], *points[2], color=COLOR_WALL, batch=self.wall_batch, width=WALL_WIDTH),
            Line(*points[3], *points[1], color=COLOR_WALL, batch=self.wall_batch, width=WALL_WIDTH),
            Line(*points[3], *points[2], color=COLOR_WALL, batch=self.wall_batch, width=WALL_WIDTH),
        ]

        self.score = Label(f"Score: 0", font_name='Corbel', font_size=15,
                           x=40, y=self.size_y * PIXEL_FOR_SQUARE - 20, batch=self.wall_batch)

    def eat_apple(self, snake):
        possible_positions = (self.apple_possible_positions - snake.tail.tail_set
                              - {snake.head_position.x * 1000 + snake.head_position.y})
        if len(possible_positions) != 0:
            index = randint(0, len(possible_positions))
            xy = list(possible_positions)[index - 1]
            self.apple_position = vector(xy // 1000, xy % 1000)
        else:
            snake.game_over = True

    def update(self, snake):
        snake.move(self)

    def draw(self, snake):
        self.window.clear()
        self.score.text = f"Score: {snake.score}"

        self.wall_batch.draw()

        get_rectangle(self.apple_position, COLOR_APPLE).draw()
        snake.draw()

        if snake.game_over:
            pass
            # Label("G A M E  O V E R", font_name='Corbel', font_size=20, bold=True,
            #       x=self.window.width // 2 - 90, y=self.window.height // 2).draw()


class Snake:
    def __init__(self):
        self.head_position = vector(randint(WALLS_GAP + 1, SIZE_X - WALLS_GAP - 1),
                                    randint(WALLS_GAP + 1, SIZE_Y - WALLS_GAP - 2))
        self.direction = vector(0, 1)

        self.tail = Snake_tail()

        self.score = 0
        self.game_over = False

    def draw(self):
        self.tail.tail_batch.draw()
        get_rectangle(self.head_position, COLOR_SNAKE_HEAD).draw()

    def move(self, map_field):
        if self.game_over:
            return

        self.tail.add(self.head_position, self.direction)

        self.head_position += self.direction
        self.game_over = self.check_game_over()

        if map_field.apple_position == self.head_position:
            self.score += 1
            map_field.eat_apple(self)
        else:
            self.tail.delete_end()

    def check_game_over(self, direction: vector = vector(0, 0)):
        return not (WALLS_GAP < self.head_position.x + direction.x < SIZE_X - WALLS_GAP
                    and WALLS_GAP < self.head_position.y + direction.y < SIZE_Y - WALLS_GAP) \
            or ((self.head_position.x + direction.x) * 1000 + self.head_position.y + direction.y) in self.tail.tail_set

    def change_direction(self, symbol):
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

        if self.tail.tail_set:
            new_poss = self.head_position + new_direction
            if new_poss.x * 1000 + new_poss.y not in self.tail.tail_set:
                self.direction = new_direction
        else:
            self.direction = new_direction


class Snake_tail:
    def __init__(self):
        self.tail_LList = LinkedList()
        self.tail_set = set()
        self.tail_batch = pyglet.graphics.Batch()

    def add(self, xy: vector, direction: vector):
        self.tail_set.add(xy.x * 1000 + xy.y)
        self.tail_LList.add_to_beginning(
            [xy,
             get_line(xy, xy + direction,
                      COLOR_SNAKE_TAIL, self.tail_batch)
             ]
        )

    def delete_end(self):
        el = vector(self.tail_LList[-1][0].x, self.tail_LList[-1][0].y)
        self.tail_LList.delete_end()
        self.tail_set.remove(el.x * 1000 + el.y)


def get_line(xy_start, xy_end, color, batch=None):
    direction = xy_end - xy_start
    direction /= direction.len() * 2 / (1 - PER_SENT_GAP)
    xy_start -= direction
    xy_end += direction

    return Line(xy_start.x * PIXEL_FOR_SQUARE, xy_start.y * PIXEL_FOR_SQUARE,
                xy_end.x * PIXEL_FOR_SQUARE, xy_end.y * PIXEL_FOR_SQUARE,
                PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP),
                color=color, batch=batch)


def get_rectangle(xy, color, batch=None):
    r = Rectangle(xy.x * PIXEL_FOR_SQUARE, xy.y * PIXEL_FOR_SQUARE,
                  PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP), PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP),
                  color=color, batch=batch)
    r.anchor_x += (PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP)) / 2
    r.anchor_y += PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP) / 2
    return r
