import math
import functools
import matplotlib.pyplot as plt
from itertools import count, islice, chain
from matplotlib.patches import Polygon as MplPolygon


def polygon_area(poly):
    poly = list(poly)
    n = len(poly)
    return abs(sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))) / 2


def polygon_perimeter(poly):
    poly = list(poly)
    n = len(poly)
    return sum(math.hypot(poly[(i + 1) % n][0] - poly[i][0], poly[(i + 1) % n][1] - poly[i][1]) for i in range(n))


def side_lengths(poly):
    poly = list(poly)
    n = len(poly)
    return [math.hypot(poly[(i + 1) % n][0] - poly[i][0], poly[(i + 1) % n][1] - poly[i][1]) for i in range(n)]


def is_convex(poly):
    poly = list(poly)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    signs = []
    n = len(poly)

    for i in range(n):
        c = cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n])
        if c != 0:
            signs.append(c > 0)

    return all(signs) or not any(signs)


def bbox(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def polygons_intersect(poly1, poly2):
    a1, b1, a2, b2 = bbox(poly1)
    c1, d1, c2, d2 = bbox(poly2)
    return not (a2 < c1 or c2 < a1 or b2 < d1 or d2 < b1)


def visualize_polygons(polygons, title=""):
    polygons = list(polygons)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect("equal")

    for poly in polygons:
        ax.add_patch(
            MplPolygon(
                poly,
                closed=True,
                edgecolor="black",
                facecolor="lightgray",
                linewidth=1.2,
                alpha=0.85,
            )
        )

    ax.autoscale_view()
    plt.grid(True)
    plt.title(title)
    plt.show()


def gen_rectangle(width=2, height=1, step=3):
    for i in count(0):
        x = i * step
        yield ((x, 0), (x + width, 0), (x + width, height), (x, height))


def gen_triangle(size=2, step=3):
    h = size * math.sqrt(3) / 2
    for i in count(0):
        x = i * step
        yield ((x, 0), (x + size / 2, h), (x + size, 0))


def gen_hexagon(radius=1, step=3):
    for i in count(0):
        cx = i * step
        yield tuple(
            (cx + radius * math.cos(math.pi / 3 * k), radius * math.sin(math.pi / 3 * k))
            for k in range(6)
        )


def tr_translate(dx, dy):
    return lambda p: tuple((x + dx, y + dy) for x, y in p)


def tr_rotate(angle, center=(0, 0)):
    angle = math.radians(angle)
    cx, cy = center

    def t(p):
        def r(v):
            x, y = v
            x -= cx
            y -= cy
            return (
                cx + x * math.cos(angle) - y * math.sin(angle),
                cy + x * math.sin(angle) + y * math.cos(angle),
            )
        return tuple(map(r, p))

    return t


def tr_symmetry(axis="x"):
    return lambda p: tuple((x, -y) for x, y in p) if axis == "x" else tuple((-x, y) for x, y in p)


def tr_homothety(k, center=(0, 0)):
    cx, cy = center
    return lambda p: tuple((cx + k * (x - cx), cy + k * (y - cy)) for x, y in p)


def flt_short_side(m):
    return lambda p: min(side_lengths(p)) < m


def flt_convex_polygon():
    return lambda p: is_convex(p)


def agr_origin_nearest(polys):
    pts = chain.from_iterable(polys)
    return functools.reduce(lambda a, b: a if a[0]**2 + a[1]**2 < b[0]**2 + b[1]**2 else b, pts)


def agr_max_side(polys):
    return functools.reduce(lambda a, p: max(a, max(side_lengths(p))), polys, 0)


def agr_min_area(polys):
    return functools.reduce(lambda a, p: min(a, polygon_area(p)), polys, float("inf"))


def agr_perimeter(polys):
    return functools.reduce(lambda a, p: a + polygon_perimeter(p), polys, 0)


def agr_area(polys):
    return functools.reduce(lambda a, p: a + polygon_area(p), polys, 0)


def zip_polygons(*its):
    for ps in zip(*its):
        if len(ps) == 2 and len(ps[0]) == 3 and len(ps[1]) == 3:
            t, b = ps
            yield (t[0], t[1], t[2], b[2], b[1], b[0])
        else:
            res = []
            for p in ps:
                res.extend(p)
            yield tuple(res)


def count_2D(r, c):
    for y in range(r):
        for x in range(c):
            yield (x, y)


def zip_tuple(*its):
    for v in zip(*its):
        yield tuple(v)


if __name__ == "__main__":

    visualize_polygons(islice(gen_rectangle(), 7), "Прямоугольники")
    visualize_polygons(islice(gen_triangle(), 7), "Треугольники")
    visualize_polygons(islice(gen_hexagon(), 7), "Шестиугольники")

    ang = 25

    band = chain(
        map(tr_rotate(ang), islice(gen_rectangle(), 8)),
        map(tr_translate(0, 4), map(tr_rotate(ang), islice(gen_rectangle(), 8))),
        map(tr_translate(0, 8), map(tr_rotate(ang), islice(gen_rectangle(), 8)))
    )

    visualize_polygons(band, "Три параллельные ленты")

    strip = chain(
        map(tr_translate(2, 2), islice(gen_rectangle(), 8)),
        map(tr_rotate(40, (8, 4)), map(tr_translate(2, 2), islice(gen_rectangle(), 8)))
    )

    visualize_polygons(strip, "Пересекающиеся ленты")

    up = islice(gen_triangle(), 8)
    low = map(tr_translate(0, -4), map(tr_symmetry("x"), islice(gen_triangle(), 8)))
    visualize_polygons(chain(up, low), "Симметричные треугольники")

    rects = gen_rectangle()
    up_sec, low_sec = [], []
    scales = [0.3 + i * 0.15 for i in range(6)]

    for i, k in enumerate(scales):
        p = tr_homothety(k)(next(rects))
        p = tr_translate(3 + i * 3, 0.8 * (3 + i * 3))(p)
        up_sec.append(p)
        low_sec.append(tr_symmetry("x")(tr_symmetry("y")(p)))

    visualize_polygons(chain(up_sec, low_sec), "Четырёхугольники между двумя прямыми")

    many = (tr_homothety(0.2 + i * 0.1)(p) for i, p in enumerate(islice(gen_rectangle(), 15)))
    many = filter(flt_convex_polygon(), many)
    many = filter(flt_short_side(1), many)

    visualize_polygons(many, "Фильтр: короткая сторона < 1")

    many2 = list(islice((tr_homothety(0.2 + i * 0.1)(p) for i, p in enumerate(islice(gen_rectangle(), 15))), 4))
    visualize_polygons(many2, "Фильтр: ≤ 4 фигуры")

    inter = []
    base = next(gen_rectangle())

    for i in range(15):
        inter.append(tr_translate(i * 0.4, i * 0.2)(base))

    res = []
    for p in inter:
        if not any(polygons_intersect(p, q) for q in res):
            res.append(p)

    visualize_polygons(res, "Фильтр: пересечения")

    up_t = islice(gen_triangle(), 6)
    low_t = map(tr_translate(0, -2), map(tr_symmetry("x"), islice(gen_triangle(), 6)))
    visualize_polygons(zip_polygons(up_t, low_t), "zip_polygons")

    test = list(islice(gen_rectangle(), 5))

    print("АГРЕГАТОРЫ:")
    print("Ближайшая точка:", agr_origin_nearest(test))
    print("Максимальная сторона:", agr_max_side(test))
    print("Минимальная площадь:", agr_min_area(test))
    print("Периметр:", agr_perimeter(test))
    print("Площадь:", agr_area(test))

    print("count_2D:", list(count_2D(3, 4)))
    print("zip_tuple:", list(zip_tuple([1, 2, 3], ['a', 'b', 'c'])))
