import time

from my_math import *
import pyglet
from math import *

window = pyglet.window.Window(width=500, height=500)
circle = pyglet.shapes.Circle

p1 = vector(window.width // 2, window.height // 2)
v1 = vector(0, 100)
alf = 0.02


@window.event
def on_draw():
    global alf
    # window.clear()
    circle(*p1, radius=8, color=(255, 255, 255)).draw()
    circle(*(p1 + v1), radius=1, color=(25, 255, 255)).draw()
    v1.rotate(alf)


pyglet.app.run()
