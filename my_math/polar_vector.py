from math import cos, sin, atan


class p_vector:
    def __init__(self, r=0.0, corner=0.0):
        self.r, self.corner = r, corner

    def __str__(self):
        print(f'p_v({self.r}; {self.corner}°)')

    def __add__(self, other):
        if isinstance(other, p_vector):
            x = cos(self.corner) * self.r + cos(other.corner) * other.r
            y = sin(self.corner) * self.r + sin(other.corner) * other.r
            if x < 0:
                fi = atan(y / x) + 180
            elif x == 0:
                if y >= 0:
                    fi = 90
                else:
                    fi = 270
            else:
                if y > 0:
                    fi = atan(y / x)
                else:
                    fi = atan(y / x) + 360

            return p_vector((x ** 2 + y ** 2) ** 0.5, fi)
