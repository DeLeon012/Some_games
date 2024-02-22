from random import randint
from my_math.Linked_list import LinkedList

import pyglet.app
from pyglet.window import Window
from pyglet.window import key
from pyglet.shapes import Rectangle
from pyglet.text import Label

# parameters
WIDTH = 1500
SIZE_X, SIZE_Y = 100, 50  # Для AI нужны четные числа
# PIXEL_FOR_SQUARE = 10
PIXEL_FOR_SQUARE = WIDTH // (SIZE_X + 6)
PER_SENT_GAP = 0.1

COLOR_WALL = (0, 250, 0)
COLOR_SNAKE_HEAD = (0, 150, 0)
COLOR_SNAKE_TAIL = (150, 150, 150)
COLOR_APPLE = (250, 0, 0)

# PERIOD = 0.02
TIMES = 1


# Mathmatics __________________________
class vector:
    def __init__(self, x=0.0, y=0.0): self.x, self.y = x, y

    def __add__(self, other): return vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other): return self.x == other.x and self.y == other.y

    def __getitem__(self, item): return [self.x, self.y][item]

    def __str__(self): return f"vector({self.x}, {self.y})"


# _____________________________________


class Map:
    def __init__(self, x=SIZE_X, y=SIZE_Y):
        self.window = Window(width=(SIZE_X + 4) * PIXEL_FOR_SQUARE,
                             height=(SIZE_Y + 4) * PIXEL_FOR_SQUARE)

        self.size_x = x
        self.size_y = y
        self.apple_position = vector(randint(3, SIZE_X), randint(3, SIZE_Y))
        self.apple_possible_positions = set(i * 1000 + j
                                            for i in range(3, SIZE_X + 1)
                                            for j in range(3, SIZE_Y + 1))

        self.wall_batch = pyglet.graphics.Batch()
        self.wall_list = list()

        for x in range(2, self.size_x + 2):
            self.wall_list.append(draw_rectangle(vector(x, 2), COLOR_WALL, self.wall_batch))
            self.wall_list.append(draw_rectangle(vector(x, SIZE_Y + 1), COLOR_WALL, self.wall_batch))
        for y in range(2, SIZE_Y + 2):
            self.wall_list.append(draw_rectangle(vector(2, y), COLOR_WALL, self.wall_batch))
            self.wall_list.append(draw_rectangle(vector(SIZE_X + 1, y), COLOR_WALL, self.wall_batch))

        self.score = Label(f"Score: 0", font_name='Corbel', font_size=15,
                           x=40, y=(self.size_y + 4) * PIXEL_FOR_SQUARE - 20, batch=self.wall_batch)

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

        draw_rectangle(self.apple_position, COLOR_APPLE).draw()
        snake.draw()

        if snake.game_over:
            pass
            # Label("G A M E  O V E R", font_name='Corbel', font_size=20, bold=True,
            #       x=self.window.width // 2 - 90, y=self.window.height // 2).draw()


class Snake:
    def __init__(self):
        self.head_position = vector(randint(3, SIZE_X - 1), randint(3, SIZE_Y - 1))
        self.direction = vector(0, 1)

        self.tail = Snake_tail()

        self.score = 0
        self.game_over = False

    def draw(self):
        draw_rectangle(self.head_position, COLOR_SNAKE_HEAD).draw()
        self.tail.tail_batch.draw()

    def move(self, map_field):
        if self.game_over:
            return

        self.tail.add(self.head_position)

        self.head_position += self.direction
        self.game_over = self.check_game_over()

        if not (map_field.apple_position == self.head_position):
            self.tail.delete_end()
        else:
            self.score += 1
            map_field.eat_apple(self)

    def check_game_over(self, direction: vector = vector(0, 0)):
        return not (3 <= self.head_position.x + direction.x <= SIZE_X
                    and 3 <= self.head_position.y + direction.y <= SIZE_Y) \
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

    def add(self, xy: vector):
        self.tail_set.add(xy.x * 1000 + xy.y)
        self.tail_LList.add_to_beginning(
            draw_rectangle(xy, COLOR_SNAKE_TAIL, self.tail_batch)
        )

    def delete_end(self):
        # print(self.tail_set)
        el = vector(self.tail_LList.tail.next.value.x, self.tail_LList.tail.next.value.y)
        self.tail_LList.delete_end()
        self.tail_set.remove(el.x / PIXEL_FOR_SQUARE * 1000 + el.y / PIXEL_FOR_SQUARE)


def draw_rectangle(xy: vector, color, wall_batch=None):
    return Rectangle(xy[0] * PIXEL_FOR_SQUARE, xy[1] * PIXEL_FOR_SQUARE,
                     PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP), PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP), color,
                     batch=wall_batch)


def change_period(k):
    global TIMES
    TIMES *= k
    print(TIMES)
