import time

from my_math import *
import pyglet
from math import *

window = pyglet.window.Window(width=500, height=500)
circle = pyglet.shapes.Circle

p1 = vector(window.width // 2, window.height // 2 + 100)
v1 = vector(50, 100)

alf = 1 * pi / 180

p2 = p1 + v1
circle(*p1, radius=2).draw()
circle(*p2, radius=2).draw()

v1 = v1 * (-110 / v1.len())
p2 = p1 + v1
circle(*p1, radius=2, color=(50, 200, 50)).draw()
circle(*p2, radius=2, color=(50, 200, 50)).draw()


pyglet.app.run()

