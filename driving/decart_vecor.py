from math import cos, sin


class vector:
    def __init__(self, x=0.0, y=0.0):
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
        return (self.x ** 2 + self.y ** 2) ** 0.5

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

    def __truediv__(self, other):
        if isinstance(other, vector):
            x = self.x / other.x
            y = self.y / other.y
        elif isinstance(other, (int, float)):
            x = self.x / other
            y = self.y / other
        else:
            raise Exception('Непонятный расчет (деление)')
        return vector(x, y)

    def __floordiv__(self, other):
        if isinstance(other, vector):
            x = self.x // other.x
            y = self.y // other.y
        elif isinstance(other, (int, float)):
            x = self.x // other
            y = self.y // other
        else:
            raise Exception('Непонятный расчет (деление)')
        return vector(x, y)

    def rotate(self, alf):
        x, y = self.x, self.y
        self.x = x * cos(alf) - y * sin(alf)
        self.y = x * sin(alf) + y * cos(alf)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError('У вектора только два индекса')

    def __str__(self):
        return f'v({self.x}, {self.y})'

    def copy(self):
        return vector(self.x, self.y)


def rotated(v: vector, angle: (float, int)):
    x, y = v.x, v.y
    return vector(x * cos(angle) - y * sin(angle), x * sin(angle) + y * cos(angle))


def cos_v(v1: vector, v2: vector):
    return (v1.x * v2.x + v1.y * v2.y) / (v1.len() * v2.len())


def sin_v(v1: vector, v2: vector):
    x1, y1 = v1.x, v1.y
    x2, y2 = v2.x, v2.y
    return (((x1 ** 2 + y1 ** 2) * (x2 ** 2 + y2 ** 2) - (x1 * x2 + y1 * y2)) ** 0.5) / (v1.len() * v2.len())


def get_color(mass):
    k = (-500) / mass + 1
    r = 240 + int((93 - 240) * k)
    g = 116 + int((127 - 116) * k)
    b = 82 + int((247 - 82) * k)
    return r, g, b
