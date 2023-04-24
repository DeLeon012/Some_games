from math import cos, sin


class vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return vector(x, y)

    def __sub__(self, other):
        if isinstance(other, vector):
            x = self.x - other.x
            y = self.y - other.y
        elif isinstance(other, int):
            x = self.x - other
            y = self.y - other
        else:
            raise Exception('Непонятный расчет (вычитание)')
        return vector(x, y)

    def len(self):
        return(self.x ** 2 + self.y ** 2) ** 0.5

    def __mul__(self, other):
        if isinstance(other, vector):
            x = self.x * other.x
            y = self.y * other.y
        elif isinstance(other, (int, float)):
            x = self.x * other
            y = self.y * other
        else:
            raise Exception('Непонятный расчет (умножение)')
        return vector(x, y)

    def rotate(self, alf):
        self.x = self.x * cos(alf) - self.y * sin(alf)
        self.y = self.x * sin(alf) + self.y * cos(alf)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError('У вектора только два индекса')

    def __str__(self):
        return f'({self.x}, {self.y})'


def cos_v(v1: vector, v2: vector):
    return (v1.x * v2.x + v1.y * v2.y) / (v1.len() * v2.len())


def sin_v(v1: vector, v2: vector):
    x1, y1 = v1.x, v1.y
    x2, y2 = v2.x, v2.y
    return (((x1 ** 2 + y1 ** 2) * (x2 ** 2 + y2 ** 2) - (x1 * x2 + y1 * y2)) ** 0.5)/(v1.len() * v2.len())
