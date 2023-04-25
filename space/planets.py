import pyglet
from my_math import *
from math import *
from random import randrange


window = pyglet.window.Window(
    # fullscreen=True,
    width=1000, height=1000
)
circle = pyglet.shapes.Circle

G = 1.5
p_V = 0.3
T = 0.01

a_contact = 0.3


class ball:
    def __init__(self, poss, v=vector(0, 0), mass=5_000, color=None, p_v=p_V, static=False):
        self.poss = poss
        self.v = v
        self.mass = mass
        self.p_v = p_v
        self.R = (3 * mass / (4 * self.p_v * pi)) ** (1 / 3)
        self.F = vector(0, 0)
        self.color = get_color(mass) if not color else color
        self.static = static

    def F_add(self, ball2):
        r = ball2.poss - self.poss
        r_len = r.len()
        F = r * (G * ball2.mass * self.mass / (r_len ** 3))
        self.F += F

        if r_len < self.R + ball2.R:
            print('Contact')
            c = cos_v(r, self.F)
            N = r * (self.F * c) / (-r_len)
            self.F += N

    def update(self):
        if not self.static:
            a = self.F / self.mass
            self.poss += self.v * T + a * (T ** 2) * 0.5
            self.v += a * T

        if self.poss.x <= self.R:
            self.v.x = abs(self.v.x)
        elif self.poss.x >= self.poss.x >= window.width - self.R:
            self.v.x = -abs(self.v.x)
        if self.poss.y <= self.R:
            self.v.y = abs(self.v.y)
        elif self.poss.y >= self.poss.y >= window.width - self.R:
            self.v.y = -abs(self.v.y)

        self.F = vector(0, 0)


def new_random_ball():
    poss = vector(randrange(window.width), randrange(window.height))
    max_v = 5
    v = vector(randrange(max_v), randrange(max_v))
    mass = randrange(500, 10_000, 100)
    return ball(poss, v, mass)


# items = [new_random_ball() for _ in range(5)]
items = [
    ball(
        vector(window.width // 2 - 150, window.height // 2),
        vector(3, 0),
        color=(200, 50, 50), static=True),
    ball(
        vector(window.width // 2 + 150, window.height // 2),
        vector(-3, 0),
        color=(50, 50, 200))
]


@window.event
def on_draw():
    window.clear()
    for i in range(len(items)):
        for j in range(len(items)):
            if i == j:
                continue
            items[i].F_add(items[j])
        if not items[i].static:
            v = (items[i].poss + (items[i].F // (items[i].F.len() + 1) * 100))
            circle(*v, radius=3, color=(200, 200, 200)).draw()

        items[i].update()
    for i in items:
        circle(*i.poss, i.R, color=i.color).draw()




if __name__ == '__main__':
    pyglet.app.run()