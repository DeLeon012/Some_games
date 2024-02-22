w = 4
h = 6

l = []
line = [0] * w
for _ in range(h):
    l.append(line.copy())


def f(x, y, w, h):
    if x == 0:
        return (h * w - y) % (h * w)

    if not (y % 2):
        return x + y * (w - 1)
    return y * (w - 1) + (w - x)


for x in range(w):
    for y in range(h):
        l[y][x] = f(x, y, w, h)

for i in l:
    print(i)
