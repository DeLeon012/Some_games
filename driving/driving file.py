import pyglet
from pyglet.window import key
from pyglet.shapes import Rectangle, Line, Circle

import math
from decart_vecor import *

# Parameters
A_FRICTION = 0.14
CAR_ROTATE = 0.1
F_CAR = 2.5
SCALE = 1.5
CAR_ROTATE_WHEEL = 7

window = pyglet.window.Window(
    # width=1200, height=800
    fullscreen=True
)
pyglet.gl.glClearColor(0.6, 0.6, 0.6, 1)


class Car:
    def __init__(self):
        self.long = 50
        self.position = vector(window.width // 2, window.height // 2)

        self.V = vector()
        self.F = 0

        self.direction = vector(0, 1)
        self.rotate = 0

    def move(self):
        self.position += self.V + (self.direction * self.F - self.V * A_FRICTION) / 2
        self.V += self.direction * self.F - self.V * A_FRICTION

        if self.V.len() != 0:
            if cos_v(self.V, self.direction) < 0:
                self.direction.rotate(-self.rotate * self.V.len() * 0.05)
            else:
                self.direction.rotate(self.rotate * self.V.len() * 0.05)
        self.direction /= self.direction.len()

        for i in self.get_corner_points():
            if not (0 <= i.x <= window.width and 0 <= i.y <= window.height):
                self.position = vector(window.width // 2, window.height // 2)

        # for i in self.get_corner_points():
        #     Circle(*i, radius=2, color=(0, 255, 0)).draw()

    def get_corner_points(self):
        return [self.position + rotated(self.direction * (10 * SCALE), math.pi / 2),
                self.position + rotated(self.direction * (10 * SCALE), -math.pi / 2),
                self.position + rotated(self.direction * (10 * SCALE), math.pi / 2) + self.direction * (50 * SCALE),
                self.position + rotated(self.direction * (10 * SCALE), -math.pi / 2) + self.direction * (50 * SCALE)]


car = Car()
image_car = pyglet.image.load('sports-car-delorean.png',
                              decoder=pyglet.image.codecs.png.PNGImageDecoder())
image_car.anchor_x = 130
image_car.anchor_y = 20


def draw_car():
    im_car = pyglet.sprite.Sprite(image_car, *car.position)
    im_car.scale = 0.1 * SCALE

    draw_wheels()
    corner_cos = cos_v(car.direction, vector(0, 1))
    if car.direction.x > 0:
        im_car.rotation = 360 + math.degrees(math.acos(corner_cos))
    else:
        im_car.rotation = -math.degrees(math.acos(corner_cos))
    im_car.draw()

    # Rectangle(*car.position, width=3, height=3, color=(255, 0, 0)).draw()
    # Rectangle(*(car.position + car.direction * 15), width=3, height=3, color=(2, 250, 0)).draw()


def draw_wheels():
    vector_replace = car.direction * 13 * SCALE
    vector_replace.rotate(0.8)

    vector_replace_2 = car.direction * 19.6 * SCALE
    vector_replace_2.rotate(-math.pi / 2)

    def draw_wheel(point, angle=0):
        height = car.direction.copy()
        height.rotate(angle)
        wheel = Line(*point, *(point + height * 8 * SCALE), width=7 * SCALE, color=(0, 0, 0))
        wheel.anchor_x += 4 * SCALE

        wheel.draw()
        # Circle(*point, radius=2, color=(0, 255, 0)).draw()

    draw_wheel(car.position + vector_replace)
    draw_wheel(car.position + vector_replace + car.direction * 30 * SCALE, car.rotate * CAR_ROTATE_WHEEL)

    draw_wheel(car.position + vector_replace + vector_replace_2)
    draw_wheel(car.position + vector_replace + car.direction * 30 * SCALE + vector_replace_2,
               car.rotate * CAR_ROTATE_WHEEL)


@window.event
def on_key_press(symbol, mod):
    if symbol == key.W:
        car.F += F_CAR
    if symbol == key.S:
        car.F += -F_CAR * 0.4
    elif symbol == key.A:
        car.rotate += CAR_ROTATE
    elif symbol == key.D:
        car.rotate += -CAR_ROTATE


@window.event
def on_key_release(symbol, mod):
    if symbol == key.W:
        car.F -= F_CAR
    if symbol == key.S:
        car.F -= -F_CAR * 0.4
    elif symbol == key.A:
        car.rotate -= CAR_ROTATE
    elif symbol == key.D:
        car.rotate -= -CAR_ROTATE


@window.event
def on_draw():
    global image_car
    window.clear()
    car.move()
    draw_car()
    # Line(*car.position, *(car.position + car.direction * 50), width=20).draw()


pyglet.app.run(1 / 60)
