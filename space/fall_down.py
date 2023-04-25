import pyglet
from my_math import *
from math import *
from random import randrange

window = pyglet.window.Window(
    # fullscreen=True,
    width=1000, height=1000
)
circle = pyglet.shapes.Circle
rectangle = pyglet.shapes.Rectangle

G = 1.5
p_V = 0.3
T = 0.05

g = 10


class ball:
    def __init__(self, poss, v=vector(0, 0), mass=5_000, color=None, p_v=p_V):
        self.poss = poss
        self.v = v
        self.mass = mass
        self.p_v = p_v
        self.R = (3 * mass / (4 * self.p_v * pi)) ** (1 / 3)
        self.F = vector(0, 0)
        self.color = get_color(mass) if not color else color

    def F_add(self, ball2):
        r = ball2.poss - self.poss
        r_len = r.len()
        if r_len <= self.R + ball2.R:
            c = cos_v(r, self.v)
            v0 = c * self.v.len()
            v2 = cos_v(r * (-1), ball2.v) * ball2.v.len()
            v1 = calc_v(v0, v2, self.mass, ball2.mass)

            v_r = r * v0 / r_len
            v_sin = self.v - v_r
            v_cos = r * (-v1/r_len)
            self.v = v_sin + v_cos

    def update(self):
        a = self.F / self.mass
        self.poss += self.v * T + a * (T ** 2) * 0.5
        self.v += a * T

        if self.poss.x <= self.R:
            self.v.x = abs(self.v.x)
        elif self.poss.x >= window.width - self.R:
            self.v.x = -abs(self.v.x)

        print(*self.v)
        self.F = vector(0, 0)


def calc_v(v1, v2, m1, m2):
    return (v1 * (m1 - m2) + v2 * m2 * 2) / (m1 + m2)


def new_random_ball():
    poss = vector(randrange(window.width), randrange(window.height))
    max_v = 5
    v = vector(randrange(max_v), randrange(max_v))
    mass = randrange(500, 10_000, 100)
    return ball(poss, v, mass)


# items = [new_random_ball() for _ in range(5)]
items = [
    ball(
        vector(window.width // 2 + 5, window.height // 2 + 100),
        vector(0, 2),
        color=(50, 50, 200), mass=7_000),
    ball(
        vector(window.width // 2, window.height // 2 - 100),
        vector(0, 10),
        color=(200, 50, 50), mass=7_000)
]


@window.event
def on_draw():
    window.clear()
    for i in range(len(items)):
        for j in range(len(items)):
            if i == j:
                continue
            items[i].F_add(items[j])

        items[i].update()
    for i in items:
        circle(*i.poss, i.R, color=i.color).draw()


if __name__ == '__main__':
    pyglet.app.run()
