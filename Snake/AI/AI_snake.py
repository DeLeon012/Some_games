# from Snake.Snake_with_AI_1_1.Classes import *
import copy

from my_math.decart_vecor import vector
from my_math.Linked_list import LinkedList
from pyglet.window import key
from pyglet.shapes import Line
import pyglet

from Snake.Snake_with_AI_1_2.configs import *
# from Snake.Snake_with_AI_1_2.Field_Snake import Map, Snake
import sys

sys.setrecursionlimit(17000)


class AI:
    def __init__(self):
        self.AI = True
        self.nextStep = None
        self.buttons_for_movies = {
            '-10': key.LEFT,
            '01': key.UP,
            '10': key.RIGHT,
            '0-1': key.DOWN,
        }

        self.total_space = (SIZE_X - 3) * (SIZE_Y - 3)
        # print(self.total_space)

        self.K = 0.06
        self.K2 = self.total_space / 2
        self.can_be_skipped = self.total_space

        self.numbers_batch = pyglet.graphics.Batch()
        self.numbers_LL = LinkedList()

        self.num_option = 1
        self.cur_num = 0
        # print(self.options)
        self.numbers_list = []
        self.make_cycle()
        self.lines_LL = LinkedList()

        if self.numbers_list:
            self.draw_numbers()
            self.get_lines()
        else:
            print("Unsuccessful")

        # self.set_numbers()
        self.is_drawing_numbers = False

    def draw_numbers(self):
        all_y, all_x = len(self.numbers_list), len(self.numbers_list[0])
        for y in range(all_y):
            for x in range(all_x):
                lab = pyglet.text.Label(str(self.numbers_list[y][x]),
                                        x=x * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                        y=y * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                        font_size=PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP) / 4,
                                        batch=self.numbers_batch)
                self.numbers_LL.add_to_end(lab)

    def set_numbers(self):
        for x in range(SIZE_X - WALLS_GAP * 2 - 1):
            for y in range(SIZE_Y - WALLS_GAP * 2 - 1):
                num = get_number_of_field(x, y)
                lab = pyglet.text.Label(str(num), x=x * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                        y=y * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                        font_size=PIXEL_FOR_SQUARE * (1 - PER_SENT_GAP) / 4,
                                        batch=self.numbers_batch)
                self.numbers_LL.add_to_end(lab)

    def get_lines(self):
        # print(self.total_space)
        i = 1
        p = vector(0, 0)
        v = [vector(1, 0), vector(0, 1), vector(-1, 0), vector(0, -1)]
        while i < self.total_space + 1:
            # print(self.total_space, i, get_number_of_field(*(p + vector(0, -1))))
            for j in v:
                # n = (p + j).x * 1000 + (p + j).y
                # if 0 <= (p + j).x < SIZE_X - WALLS_GAP * 2 - 1 \
                #         and 0 <= (p + j).y < SIZE_Y - WALLS_GAP * 2 - 1:
                try:
                    if (self.numbers_list[(p + j).y][(p + j).x] - i == 1
                            or i - self.numbers_list[(p + j).y][(p + j).x] == self.total_space - 1):
                        self.lines_LL.add_to_end(
                            Line(p.x * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                 p.y * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                 (p + j).x * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                 (p + j).y * PIXEL_FOR_SQUARE + WALLS_GAP * PIXEL_FOR_SQUARE * 2,
                                 width=2, color=COLOR_WALL, batch=self.numbers_batch)
                        )
                        p += j
                        i += 1
                        break
                    # else:
                    #     print(self.numbers_list[(p + j).y][(p + j).x])
                except IndexError:
                    continue
            # print(i)

    def update_can_be_skipped(self, score):
        self.can_be_skipped = self.total_space - score * 20

    def make_step(self, vec, snake):
        if snake.direction != vec:
            move_str = str(vec[0]) + str(vec[1])
            self.nextStep = self.buttons_for_movies[move_str]
            # print(for_debug[move_str])
        else:
            self.nextStep = None

    def next_step(self, snake, map_field):
        # print(snake.head_position, map_field.apple_position)
        current = self.numbers_list[snake.head_position.y - 2][snake.head_position.x - 2]
        # print(current, snake.head_position)
        apple = self.numbers_list[map_field.apple_position.y - 2][map_field.apple_position.x - 2]
        way_to_apple = self.get_distance(apple, current)

        # print(current)

        moves = [vector(1, 0), vector(-1, 0), vector(0, 1), vector(0, -1)]
        options = []
        for i in moves:
            try:
                new_poss = self.numbers_list[(snake.head_position + i).y - 2][(snake.head_position + i).x - 2]
                if not (i + snake.direction == vector(0, 0)) \
                        and not snake.check_game_over(i):
                    options.append([new_poss, i])
            except IndexError:
                continue

        filtered_options = []
        for i in options:
            new_poss, vec = i
            skip = self.get_distance(new_poss, current) - 1

            if self.is_skippable(skip, snake, current) \
                    and skip < way_to_apple:
                filtered_options.append([new_poss, skip, vec])

        try:
            move_vector = max(filtered_options, key=lambda x: x[1])[2]
            self.make_step(move_vector, snake)
        except ValueError:
            print("Нет ходов")
            snake.game_over = True

    def is_skippable(self, skip, snake, current):
        # if skip == 0:
        #     return True
        # if snake.score and self.can_be_skipped > 0:
        #     last_tail = vector(snake.tail.tail_LList.tail.next.value.x, snake.tail.tail_LList.tail.next.value.y)
        #     last_tail_num = get_number_of_field(*last_tail)
        #     distance_to_last_tail = get_distance(last_tail_num, current)
        #     if distance_to_last_tail < (self.total_space - snake.score) * 0.1:
        #         self.can_be_skipped -= self.total_space * 0.005
        #         print(self.can_be_skipped)
        #     if self.can_be_skipped < 0:
        #         self.can_be_skipped = 0
        # return skip < self.can_be_skipped
        # return skip < (self.K2 / (snake.score * 0.12 + 1))
        return skip / (self.total_space - snake.score - 1) < self.K

    def add_option(self, p):
        p_new = copy.deepcopy(p)
        self.cur_num += 1
        self.numbers_list = p_new
        print(self.cur_num)
        return self.cur_num >= self.num_option

    def make_cycle(self):
        points = [None] * (SIZE_Y - 3)

        line = [None] * (SIZE_X - 3)
        for i in range(len(points)):
            points[i] = line.copy()

        start = vector(0, 0)
        self.requaction(start, 1, points, self.total_space)

    def requaction(self, point: vector, i, points: list, total):
        if not (0 <= point.x < (SIZE_X - 3) and 0 <= point.y < (SIZE_Y - 3)) \
                or points[point.y][point.x]:
            return False

        # sh(points)
        if i == total and (points[point.y - 1][point.x] == 1 or points[point.y][point.x - 1] == 1):
            points[point.y][point.x] = i
            l = self.add_option(points)
            points[point.y][point.x] = None

            return l

        elif i == total or (
                (points[point.y - 1][point.x] == 1 or points[point.y][
                    point.x - 1] == 1) and i != 2):
            # print("fatal")
            return False
        else:
            points[point.y][point.x] = i

            if not check_split(point.x, point.y, points, i):
                # print('been', point)
                # sh(points)
                points[point.y][point.x] = None
                return False

            o = vectors_3
            if i == 146 or i == 214:
                o = vectors_4
                print('replace')
                # sh(points)
            for j in o:
                # print(j)
                if self.requaction(point + j, i + 1, points, total):
                    return True
            points[point.y][point.x] = None
            return False

    def get_distance(self, a, b):
        return (a if a > b else a + self.total_space) - b


def check_split(x, y, m, i):
    p1, p2, p3, p4 = None, None, None, None
    if x == 0:
        p1 = 1
        p3 = 1 if m[y][x + 1] else None
    elif x == len(m[0]) - 1:
        p3 = 1
        p1 = 1 if m[y][x - 1] else None
    else:
        if m[y][x - 1]: p1 = 1
        if m[y][x + 1]: p3 = 1

    if y == 0:
        p2 = 1
        if m[y + 1][x]: p4 = 1
    elif y == len(m) - 1:
        p4 = 1
        if m[y - 1][x]: p2 = 1
    else:
        # print(x, y)
        if m[y - 1][x]: p2 = 1
        if m[y + 1][x]: p4 = 1

    if p1 and p3 and not p2 and not p4:
        return get_square(x, y + 1, m) == len(m) * len(m[0]) - i
    elif p2 and p4 and not p1 and not p3:
        return get_square(x + 1, y, m) == len(m) * len(m[0]) - i
    else:
        return True


st = {
    'back': (SIZE_X - 3) * (SIZE_Y - 3) - 10,
    "start": False,
    'count': 20,
    'now': 0
}


def get_number(xy: vector):
    return get_number_of_field(*(xy + vector(-2, -2)))


def get_number_of_field(x, y, w=SIZE_X - 3, h=SIZE_Y - 3):
    if x == 0:
        return (h * w - y) % (h * w)
    if not (y % 2):
        return x + y * (w - 1)
    return y * (w - 1) + (w - x)


def sh(p):
    s = ''
    for i in p:
        for j in i:
            if not j: j_s = '    '
            else: j_s = str(j)
            s += ' ' * (4 - len(j_s)) + j_s + ' '
        s += '\n'
    print(s)


def get_square(x, y, m, already=None, count=0):
    if not already:
        already = set()

    try:
        if y * 1000 + x not in already and not m[y][x] and y >= 0 and x >= 0:
            already.add(y * 1000 + x)
            count += 1
        else:
            return
    except IndexError:
        return

    get_square(x, y + 1, m, already, count)
    get_square(x + 1, y, m, already, count)
    get_square(x, y - 1, m, already, count)
    get_square(x - 1, y, m, already, count)
    return len(already)


vectors = [vector(-1, 0), vector(0, 1), vector(1, 0), vector(0, -1)]
vectors_2 = [vector(0, -1), vector(-1, 0), vector(0, 1), vector(1, 0)]
vectors_3 = [vector(0, 1), vector(1, 0), vector(0, -1), vector(-1, 0)]
vectors_4 = [vector(-1, 0), vector(0, 1), vector(1, 0), vector(0, -1)]
