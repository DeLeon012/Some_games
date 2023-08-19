import pyglet
from my_math import *
from math import *
from random import randrange

window = pyglet.window.Window(
    fullscreen=True
    # width=1500, height=900
)
circle = pyglet.shapes.Circle

G = 1
p_V = 0.3
T = 0.2
k = 500
n = 1


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
        ball2.F += r * (-F)
        if r_len <= self.R + ball2.R:
            v01 = cos_v(self.v, r) * self.v.len()
            v02 = cos_v(ball2.v, r) * ball2.v.len()
            P1 = - 2 * self.mass * ball2.mass * (v02 - v01) / (self.mass + ball2.mass)
            self.v += r * (-1) * (P1 / self.mass) * n
            ball2.v += r * (P1 / ball2.mass) * n

    def update(self):
        if not self.static:
            a = self.F / self.mass
            self.poss += self.v * T + a * (T ** 2) * 0.5
            self.v += a * T

        if self.poss.x < 0 or self.poss.x > window.width:
            self.poss.x = window.width - self.poss.x
        if self.poss.y < 0 or self.poss.y > window.height:
            self.poss.y = window.height - self.poss.y

        self.F = vector(0, 0)


def new_random_ball():
    poss = vector(randrange(window.width), randrange(window.height))
    max_v = 5
    v = vector(randrange(max_v), randrange(max_v))
    mass = randrange(500, 10_000, 100)
    return ball(poss, v, mass)


def get_system_impulse():
    Px, Py = 0, 0
    for i in items:
        Px += i.mass * i.v.x
        Py += i.mass * i.v.y
    return vector(Px, Py)


def get_leveling_ball():
    mass = 2_000
    v = get_system_impulse() / mass
    poss = vector(randrange(window.width), randrange(window.height))
    return ball(poss, v, mass)


items = [new_random_ball() for _ in range(5)]


count = 0

@window.event
def on_draw():
    global count
    window.clear()
    for i in range(len(items) - 1):
        for j in range(i + 1, len(items)):
            items[i].F_add(items[j])
    for i in items:
        i.update()
        circle(*i.poss, i.R, color=i.color).draw()
        if i.poss.x <= i.R or i.poss.x >= window.width - i.R:
            x = window.width + i.poss.x
            circle(*vector(x, i.poss.y), i.R, color=i.color).draw()
        if i.poss.y <= i.R or i.poss.y >= window.height - i.R:
            y = window.height + i.poss.y
            circle(*vector(i.poss.x, y), i.R, color=i.color).draw()
        if count == 200:
            print(get_system_impulse().len())
            count = 0
        count += 1


if __name__ == '__main__':
    pyglet.app.run()
