import time

import pyglet
from my_math import *
from math import *
import keyboard

window = pyglet.window.Window(width=1000, height=1000, fullscreen=False)
circle = pyglet.shapes.Circle

G = 10 ** (-2)
p_V = 0.3
T = 0.5

STOP = False


class ball:
    def __init__(self, poss, v=vector(5, 5), mass=5_000, color=(200, 200, 200), p_v1=p_V):
        self.poss = poss
        self.v = v
        self.mass = mass
        self.p_v = p_v1
        self.R = (3 * mass / (4 * self.p_v * pi)) ** (1 / 3)
        self.a = vector(0, 0)
        self.color = color

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


items = [
    ball(vector(window.width // 2 + 50, window.height // 2), v=vector(0, 5), color=(200, 50, 50)),
    ball(vector(window.width // 2 - 50, window.height // 2), v=vector(0, -5), color=(50, 200, 50)),
    ball(vector(window.width // 2 - 50, window.height // 2 - 50), v=vector(-5, 0), color=(50, 50, 200))
]


@window.event
def on_draw():
    window.clear()

    for i in items:
        circle(*i.poss, i.R, color=i.color).draw()

    while STOP:
        time.sleep(0.5)

    for i in range(len(items)):
        for j in range(len(items)):
            if i == j:
                continue
            items[i].F(items[j])
        items[i].update()


def f(arg):
    global STOP
    print(f'Нажали {arg}')
    STOP = arg


if __name__ == '__main__':
    keyboard.add_hotkey('ctrl', f, args=True)
    keyboard.add_hotkey('alt', f, args=False)
    pyglet.app.run()
