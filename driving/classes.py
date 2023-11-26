from my_math.decart_vecor import *
import math
import pyglet


class Player:
    def __init__(self):
        self.laps = []
        self.count_of_dies = 0
        self.checkpoint = False


class Car:
    def __init__(self, scale):
        self.scale = scale
        self.position = vector(90, 435)

        self.V = vector()
        self.F = 0

        self.direction = vector(0, 1)
        self.rotate = 0

    def move(self, a_friction):
        self.V += self.direction * self.F - self.V * a_friction
        self.position += self.V

        if self.V.len() != 0:
            if cos_v(self.V, self.direction) < 0:
                self.direction.rotate(-self.rotate * self.V.len() * 0.05)
            else:
                self.direction.rotate(self.rotate * self.V.len() * 0.05)
        self.direction /= self.direction.len()

    def get_corner_points(self):
        return [self.position + rotated(self.direction * (10 * self.scale), math.pi / 2),
                self.position + rotated(self.direction * (10 * self.scale), -math.pi / 2),
                self.position + rotated(self.direction * (10 * self.scale),
                                        math.pi / 2) + self.direction * (50 * self.scale),
                self.position + rotated(self.direction * (10 * self.scale),
                                        -math.pi / 2) + self.direction * (50 * self.scale)]

    def lines(self):
        points = self.get_corner_points()
        return [[points[2], points[0]], [points[3], points[1]]]

    def restart(self):
        self.position = vector(90, 435)
        self.V = vector(0, 0)
        self.direction = vector(0, 1)

    def draw_car(self, image_car, car_rotate_wheel):
        im_car = pyglet.sprite.Sprite(image_car, *self.position)
        im_car.scale = 0.1 * self.scale

        vector_replace = self.direction * 13 * self.scale
        vector_replace.rotate(0.8)

        vector_replace_2 = self.direction * 19.6 * self.scale
        vector_replace_2.rotate(-math.pi / 2)

        def draw_wheel(point, angle=0):
            height = self.direction.copy()
            height.rotate(angle)
            wheel = pyglet.shapes.Line(*point, *(point + height * 8 * self.scale), width=7 * self.scale,
                                       color=(0, 0, 0))
            wheel.anchor_x += 4 * self.scale

            wheel.draw()

        draw_wheel(self.position + vector_replace)
        draw_wheel(self.position + vector_replace + self.direction * 30 * self.scale, self.rotate * car_rotate_wheel)

        draw_wheel(self.position + vector_replace + vector_replace_2)
        draw_wheel(self.position + vector_replace + self.direction * 30 * self.scale + vector_replace_2,
                   self.rotate * car_rotate_wheel)

        corner_cos = cos_v(self.direction, vector(0, 1))
        if self.direction.x > 0:
            im_car.rotation = 360 + math.degrees(math.acos(corner_cos))
        else:
            im_car.rotation = -math.degrees(math.acos(corner_cos))
        im_car.draw()

    def __str__(self):
        return f'Car: position: {self.position}, speed: {self.V}, rotation: {self.rotate}, F: {self.F}'
