import pyglet
from my_math import *
from math import *


window = pyglet.window.Window(
    fullscreen=True)
circle = pyglet.shapes.Circle

G = 5
p_V = 0.3
T = 0.5

STOP = False


class ball:
    def __init__(self, poss, v=vector(5, 5), mass=5_000, color=None, p_v1=p_V):
        self.poss = poss
        self.v = v
        self.mass = mass
        self.p_v = p_v1
        self.R = (3 * mass / (4 * self.p_v * pi)) ** (1 / 3)
        self.a = vector(0, 0)
        self.color = get_color(mass) if not color else color

    def F(self, ball2):
        r = ball2.poss - self.poss
        r_len = r.len()
        if r_len < self.R + ball2.R:
            r_len = self.R + ball2.R
        a = G * ball2.mass / (r_len ** 2)
        self.a.x += a * r.x / r_len
        self.a.y += a * r.y / r_len

    def update(self):
        self.poss += self.v * T + self.a * (T ** 2) * 0.5
        self.v += self.a * T

        if self.poss.x <= self.R or self.poss.x >= window.width - self.R:
            self.v.x *= -1
        if self.poss.y <= self.R or self.poss.y >= window.height - self.R:
            self.v.y *= -1

        self.a = vector(0, 0)


def get_color(mass):
    k = (-778) / (mass + 778) + 1
    r = 240 + int((93 - 240) * k)
    g = 116 + int((127 - 116) * k)
    b = 82 + int((247 - 82) * k)
    return r, g, b


items = [
    ball(vector(window.width // 2 + 50, window.height // 2), v=vector(0, 5), mass=7000),
    ball(vector(window.width // 2 - 50, window.height // 2), v=vector(0, -5), mass=5000),
    ball(vector(window.width // 2 - 50, window.height // 2 - 50), v=vector(-5, 0), mass=1000)
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
