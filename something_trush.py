import pyglet
from pyglet import shapes

window = pyglet.window.Window(500, 500)
batch = pyglet.graphics.Batch()

# red_sequare = shapes.Rectangle(150, 240, 200, 20, color=(255, 55, 55), batch=batch)
# green_sequare = shapes.Rectangle(175, 220, 150, 20, color=(55, 255, 55), batch=batch)
# blue_sequare = shapes.Rectangle(200, 200, 100, 20, color=(55, 55, 255), batch=batch)

shapes.Rectangle(150, 240, 200, 20, color=(255, 55, 55), batch=batch)
shapes.Rectangle(175, 220, 150, 20, color=(55, 255, 55), batch=batch)
shapes.Rectangle(200, 200, 100, 20, color=(55, 55, 255), batch=batch)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()