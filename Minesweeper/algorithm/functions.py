import random


class Map:
    def __init__(self, height, width, numbers, pixel_cell):
        self.height, self.width, self.NUMBERS, self.pixel_cell = height, width, numbers, pixel_cell
        self.map = []
        for i in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(Cell())
            self.map.append(line)
        self.game_over = False
        self.moves_queue = set()

    def update(self, cells, game_over):
        # print('update')
        self.game_over = game_over
        for i in cells:
            cell = Cell(number=self.get_number(i), opened=True)
            x, y = i // 1000 // self.pixel_cell, i % 1000 // self.pixel_cell
            self.map[y][x] = cell

        self.analise_flag()
        # self.draw()
        self.analise_open()

    def get_number(self, xy):
        for i in self.NUMBERS:
            for j in self.NUMBERS[i]:
                if j == xy:
                    return int(i)

    def draw(self):
        text = ''
        for i in self.map[::-1]:
            line = ''
            for j in i:
                if j.flag:
                    line += 'P' + ' '
                elif j.opened:
                    line += str(j.number) + ' ' if j.number else '  '
                else:
                    line += 'X' + ' '
            line += '\n'
            text += line
        print(text)

    def analise_flag(self):
        # print('analise_flag')
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].number:
                    hidden, flags = check_around(j, i, self.map)
                    if len(hidden) + len(flags) == self.map[i][j].number:
                        for k in hidden:
                            an_i, an_j = int(k[:2]), int(k[2:])
                            self.map[i + an_j][j + an_i].probability = 1
                            if not self.map[i + an_j][j + an_i].flag:
                                self.map[i + an_j][j + an_i].flag = True
                                # self.moves_queue.append(Move(j + an_i, i + an_j, 4))
                                self.moves_queue.add((j + an_i) * 1000 + (i + an_j) * 10 + 4)

    def analise_open(self):
        # print('analise open')
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].number:
                    hidden, flags = check_around(j, i, self.map)
                    if len(flags) == self.map[i][j].number and len(hidden) != 0:
                        self.moves_queue.add(j * 1000 + i * 10 + 1)
                        for k in hidden:
                            an_i, an_j = int(k[:2]), int(k[2:])
                            self.map[i + an_j][j + an_i].opened = True

    def send_moves(self):
        # print('send_moves')
        moves_list = [[i // 1000, i % 1000 // 10, i % 10] for i in self.moves_queue]
        # if len(moves_list) == 0:
        #     hidden_cells = set()
        #     for i in range(self.height - 1):
        #         for j in range(self.width - 1):
        #             if not self.map[i][j].opened:
        #                 hidden_cells.add(j * 1000 + i)
        #     hidden_cells = list(hidden_cells)
        #     random_cell = hidden_cells[random.randint(0, len(hidden_cells) - 1)]
        #     moves_list = [[random_cell // 1000, random_cell % 1000, 1]]

        self.moves_queue.clear()
        return moves_list


class Cell:
    def __init__(self, flag=False, number=None, opened=False, probability=None):
        self.flag = flag
        self.number = number
        self.probability = probability
        self.opened = opened


class Move:
    def __init__(self, x, y, button):
        self.x, self.y = x, y
        self.button = button


def check_around(x, y, field):
    count_not_opened, count_flags = set(), set()
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if (i == 0 and j == 0) or \
                    not (0 <= y + j < len(field)) or not (0 <= x + i < len(field[0])):
                continue
            if field[y + j][x + i].flag:
                # print('this is flag')
                count_flags.add('0' * (2 - len(str(i))) + str(i) + '0' * (2 - len(str(j))) + str(j))
            elif not field[y + j][x + i].opened:
                count_not_opened.add('0' * (2 - len(str(i))) + str(i) + '0' * (2 - len(str(j))) + str(j))

    return count_not_opened, count_flags
