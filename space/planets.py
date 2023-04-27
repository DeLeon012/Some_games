import pyglet
from my_math import *
from math import *
from random import randrange


window = pyglet.window.Window(
    # fullscreen=True,
    width=1000, height=1000
)
circle = pyglet.shapes.Circle

G = 1
p_V = 0.3
T = 0.5
k = 2_000


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
        r /= r_len
        F = G * ball2.mass * self.mass / (r_len ** 2)
        self.F += r * F
        if r_len < self.R + ball2.R:
            delta = self.R + ball2.R - r_len
            self.F += r * (-k * delta)

    def update(self):
        if not self.static:
            a = self.F / self.mass
            self.poss += self.v * T + a * (T ** 2) * 0.5
            self.v += a * T

        if self.poss.x <= self.R:
            self.v.x = abs(self.v.x)
        elif self.poss.x >= window.width - self.R:
            self.v.x = -abs(self.v.x)
        if self.poss.y <= self.R:
            self.v.y = abs(self.v.y)
        elif self.poss.y >= window.height - self.R:
            self.v.y = -abs(self.v.y)

        self.F = vector(0, 0)


def new_random_ball():
    poss = vector(randrange(window.width), randrange(window.height))
    max_v = 5
    v = vector(randrange(max_v), randrange(max_v))
    mass = randrange(500, 10_000, 100)
    return ball(poss, v, mass)


def get_leveling_ball():
    Px, Py = 0, 0
    for i in items:
        Px += i.mass * i.v.x
        Py += i.mass * i.v.y
    mass = 2_000
    v = vector(-Px / mass, -Py / mass)
    poss = vector(randrange(window.width), randrange(window.height))
    return ball(poss, v, mass)


# items = [new_random_ball() for _ in range(6)]
# items.append(get_leveling_ball())
items = [
    ball(static=True,
         poss=vector(window.width // 2 - 100, window.height // 2), v=vector(0, 0), mass=2_000, color=(50, 200, 50)),
    ball(poss=vector(window.width // 2 + 100, window.height // 2), v=vector(-5, 0), mass=2_000, color=(50, 50, 200))
]


@window.event
def on_draw():
    window.clear()
    for i in range(len(items)):
        for j in range(len(items)):
            if not i == j:
                items[i].F_add(items[j])
    for i in items:
        i.update()
        circle(*i.poss, i.R, color=i.color).draw()
        # print(i.v)


if __name__ == '__main__':
    pyglet.app.run()
