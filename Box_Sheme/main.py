import pyglet
from pyglet.shapes import Rectangle, Circle, Line
from pyglet.text import Label
from itertools import product

window = pyglet.window.Window(
    width=950, height=500
)


class Line_direct(Line):
    def __init__(self, start_point, end_point):
        super().__init__(x=start_point.x, y=start_point.y, x2=end_point.x, y2=end_point.y, width=3)
        self.x, self.y = start_point.x, start_point.y
        self.x2, self.y2 = end_point.x, end_point.y
        if start_point.active:
            self.color = (229, 43, 80)
        else:
            self.color = (120, 219, 226)
        self.start = start_point
        self.end = end_point
        self.end.active = start_point.active

    def update(self):
        if self.start.active:
            self.color = (229, 43, 80)
        else:
            self.color = (120, 219, 226)
        self.end.active = self.start.active


class Line_opposite(Line_direct):
    def __init__(self, start_point, end_point):
        super().__init__(start_point, end_point)
        end_point.active = not start_point.active

    def draw(self):
        super().draw()
        Circle(self.x2, self.y2, self._width + 4, color=self.color).draw()
        Circle(self.x2, self.y2, self._width + 2, color=(0, 0, 0)).draw()

    def update(self):
        super().update()
        self.end.active *= -1


class Box_or(Rectangle):
    def __init__(self, center_point):
        super().__init__(x=center_point.x, y=center_point.y, width=150, height=100)
        self.x, self.y = center_point.x, center_point.y
        self.input_1 = Point(center_point.x + 5, center_point.y + 80)
        self.input_2 = Point(center_point.x + 5, center_point.y + 50)
        self.input_3 = Point(center_point.x + 5, center_point.y + 20)

        self.output = Point(center_point.x + 145, center_point.y + 50)

    def update(self):
        self.output.active = self.input_1.active or self.input_2.active or self.input_3.active

    def draw(self):
        super().draw()
        Rectangle(self.x + 5, self.y + 5, width=self.width - 10, height=self.height - 10, color=(0, 0, 0)).draw()
        Label('1' if self.output.active else '0', font_name='Times New Roman', font_size=18,
              x=self.x + 75, y=self.y + 50).draw()


class Point:
    def __init__(self, x=0, y=0, active=0):
        self.x, self.y, self.active = x, y, active


point_A = Point(100, 395, 1)
point_B = Point(100, 365, 0)
point_C = Point(100, 335, 1)

point_1_1 = Point(270, point_A.y)
point_2_1 = Point(240, point_B.y)
point_3_1 = Point(210, point_C.y)

point_1_2 = Point(360, point_A.y)
point_2_2 = Point(330, point_B.y)
point_3_2 = Point(300, point_C.y)

point_1_3 = Point(point_1_1.x, point_1_1.y - 240)
point_2_3 = Point(point_2_1.x, point_2_1.y - 240)
point_3_3 = Point(point_3_1.x, point_3_1.y - 240)

point_1_4 = Point(point_1_2.x, point_1_2.y - 120)
point_2_4 = Point(point_2_2.x, point_2_2.y - 120)
point_3_4 = Point(point_3_2.x, point_3_2.y - 120)

box_1 = Box_or(Point(500, 315))
box_2 = Box_or(Point(500, 195))
box_3 = Box_or(Point(500, 75))
box_4 = Box_or(Point(700, 315))

list_of_lines = []


def update():
    global list_of_lines
    list_of_lines = \
        [Line_direct(point_A, point_1_1), Line_direct(point_1_1, point_1_2), Line_direct(point_1_2, box_1.input_1),
         Line_direct(point_B, point_2_1), Line_direct(point_2_1, point_2_2),
         Line_opposite(point_2_2, box_1.input_2),
         Line_direct(point_C, point_3_1), Line_direct(point_3_1, point_3_2),
         Line_opposite(point_3_2, box_1.input_3),

         Line_direct(point_1_1, point_1_3), Line_direct(point_2_1, point_2_3), Line_direct(point_3_1, point_3_3),
         Line_direct(point_1_3, box_3.input_1), Line_direct(point_2_3, box_3.input_2),
         Line_opposite(point_3_3, box_3.input_3),

         Line_direct(point_1_2, point_1_4), Line_direct(point_2_2, point_2_4), Line_direct(point_3_2, point_3_4),
         Line_direct(point_1_4, box_2.input_1), Line_opposite(point_2_4, box_2.input_2),
         Line_direct(point_3_4, box_2.input_3),

         Line_direct(box_1.output, box_4.input_1), Line_direct(box_2.output, box_4.input_2),
         Line_direct(box_3.output, box_4.input_3),
         Line_direct(box_4.output, Point(box_4.output.x + 50, box_4.output.y))
         ]
    box_1.update(), box_2.update(), box_3.update()
    for i in list_of_lines:
        i.update()
    box_4.update()
    list_of_lines[-1].update()


input_data = list(product((0, 1), repeat=3))
index = 0


@window.event
def on_draw():
    global index
    window.clear()
    point_A.active, point_B.active, point_C.active = input_data[index]

    update()
    for i in (('A', point_A), ('B', point_B), ('C', point_C)):
        Label(f'{i[0]}    {i[1].active}', font_name='Times New Roman', font_size=18, x=i[1].x - 10, y=i[1].y + 5).draw()

    box_1.draw(), box_2.draw(), box_3.draw(), box_4.draw()
    for line in list_of_lines:
        line.draw()

    index = (index + 1) % len(input_data)


if __name__ == '__main__':
    pyglet.app.run(2)
