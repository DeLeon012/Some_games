import pyglet
from my_math import *
from math import *
from random import randrange


window = pyglet.window.Window(
    fullscreen=True)
circle = pyglet.shapes.Circle

G = 1
p_V = 0.3
T = 1

a_contact = 0.3


class ball:
    def __init__(self, poss, v=vector(5, 5), mass=5_000, color=None, p_v=p_V):
        self.poss = poss
        self.v = v
        self.mass = mass
        self.p_v = p_v
        self.R = (3 * mass / (4 * self.p_v * pi)) ** (1 / 3)
        self.a = vector(0, 0)
        self.color = get_color(mass) if not color else color

    def F(self, ball2):
        r = ball2.poss - self.poss
        r_len = r.len()
        a = G * ball2.mass / (r_len ** 2)
        self.a.x += a * r.x / r_len
        self.a.y += a * r.y / r_len

        if r_len < self.R + ball2.R:
            self.a = r * (-a_contact / r_len)

    def update(self):
        self.poss += self.v * T + self.a * (T ** 2) * 0.5
        self.v += self.a * T

        if self.poss.x <= self.R or self.poss.x >= window.width - self.R:
            self.v.x *= -1
        if self.poss.y <= self.R or self.poss.y >= window.height - self.R:
            self.v.y *= -1

        self.a = vector(0, 0)


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
        vector(5, 0),
        color=(200, 50, 50)),
    ball(
        vector(window.width // 2 + 150, window.height // 2),
        vector(-5, 0),
        color=(50, 50, 200))
]

@window.event
def on_draw():
    window.clear()
    for i in range(len(items)):
        for j in range(len(items)):
            if i == j:
                continue
            items[i].F(items[j])
        items[i].update()
    for i in items:
        circle(*i.poss, i.R, color=i.color).draw()


if __name__ == '__main__':
    pyglet.app.run()
