"""
This module deals with the conversion of color codes.
HSV/HSB or RGB or CMYK or HSL

__author__ = prmpsmart@gmail.com
"""
from math import acos, pi, sqrt

__author__ = "prmpsmart@gmail.com"

HEX = ("A", "B", "C", "D", "E", "F")
H = 16
N = 9
TFF = 255


def hexing(m: int):
    if m > N:
        i = m - N - 1
        m = HEX[i]
    return str(m)


def int2hex(num: int) -> str:
    res = ""
    num = int(num)
    while num >= H:
        m = num % H
        res = hexing(m) + res
        num //= H
    res = hexing(num) + res
    return res


def hex2int(hex: str) -> int:
    hex = hex.upper()
    l = len(hex)
    num = 0
    for h in hex:
        if h in HEX:
            h = HEX.index(h) + 1 + N
        h = int(h)
        l -= 1
        num += h * H ** l
    return num


def hue(r: int, g: int, b: int) -> str:
    n = r - (g / 2) - (b / 2)
    d = (r ** 2) + (g ** 2) + (b ** 2) - (r * g) - (r * b) - (g * b)
    gb = 0
    if d:
        gb = acos((n / sqrt(d))) * 180 / pi
        if b > g:
            gb -= 360
    return abs(gb)


def rgb2hex(r: int, g: int, b: int) -> str:
    r = int2hex(r).zfill(2)
    g = int2hex(g).zfill(2)
    b = int2hex(b).zfill(2)
    return f"#{r}{g}{b}"


def rgb2hsl(r: int, g: int, b: int) -> tuple[int, int, int]:
    M = max([r, g, b])
    m = min([r, g, b])
    d = (M - m) / TFF
    l = (M + m) / (TFF * 2)

    if l == 0:
        s = 0
    else:
        s = d / (1 - abs((2 * l) - 1))
    h = hue(r, g, b)
    return h, s, l


def rgb2hsv(r: int, g: int, b: int) -> tuple[int, int, int]:
    M = max([r, g, b])
    m = min([r, g, b])
    v = M / TFF
    s = 0
    if M == 0:
        s = 0
    else:
        s = 1 - (m / M)
    h = hue(r, g, b)
    return h, s, v


rgb2hsb = rgb2hsv


def rgb2cmyk(r: int, g: int, b: int) -> tuple[int, int, int, int]:
    k = 1 - (max([r, g, b]) / TFF)
    k1 = 1 - k
    lbd = lambda value: (k1 - (value / TFF)) / k1
    c = lbd(r)
    m = lbd(g)
    y = lbd(b)
    return c, m, y, k


def zfill(l: str) -> str:
    return l.zfill(2)


def hex2rgb(hex: str) -> tuple[int, int, int]:
    hex = hex.replace("#", "")
    if len(hex) == 3:
        _hex = ""
        for l in hex:
            _hex += zfill(l)
        hex = _hex

    r = hex2int(hex[:2])
    g = hex2int(hex[2:4])
    b = hex2int(hex[4:6])
    return r, g, b


def hex2hsl(hex: str) -> tuple[int, int, int]:
    r, g, b = hex2rgb(hex)
    return rgb2hsl(r, g, b)


def hex2hsv(hex: str) -> tuple[int, int, int]:
    r, g, b = hex2rgb(hex)
    return rgb2hsv(r, g, b)


hex2hsb = hex2hsv


def hex2cmyk(hex: str) -> tuple[int, int, int, int]:
    r, g, b = hex2rgb(hex)
    return rgb2cmyk(r, g, b)


def hsl2hex(h: int, s: int, l: int) -> str:
    r, g, b = hsl2rgb(h, s, l)
    return rgb2hex(r, g, b)


def hsl2rgb(h: int, s: int, l: int) -> tuple[int, int, int]:
    d = s * (1 - abs((2 * l) - 1))
    m = TFF * (l - (d / 2))
    x = d * (1 - abs(((h / 60) % 2) - 1))

    if 0 <= h < 60:
        r = (TFF * d) + m
        g = (TFF * x) + m
        b = m
    elif 60 <= h < 120:
        r = (TFF * x) + m
        g = (TFF * d) + m
        b = m
    elif 120 <= h < 180:
        r = m
        g = (TFF * d) + m
        b = (TFF * x) + m
    elif 180 <= h < 240:
        r = m
        g = (TFF * x) + m
        b = (TFF * d) + m
    elif 240 <= h < 300:
        r = (TFF * x) + m
        g = m
        b = (TFF * d) + m
    elif 300 <= h < 360:
        r = (TFF * d) + m
        g = m
        b = (TFF * x) + m

    return r, g, b


def hsl2hsv(h: int, s: int, l: int) -> tuple[int, int, int]:
    v = l + (s * min([l, 1 - l]))
    if v == 0:
        s = 0
    else:
        s = 2 * (1 - (l / v))
    return h, s, v


hsl2hsb = hsl2hsv


def hsl2cmyk(h: int, s: int, l: int) -> tuple[int, int, int, int]:
    c, m, y, k = hsl2rgb(h, s, l)
    return rgb2cmyk(c, m, y, k)


def hsv2hex(h: int, s: int, v: int) -> str:
    r, g, b = hsv2rgb(h, s, v)
    return rgb2hex(r, g, b)


hsb2hex = hsv2hex


def hsv2rgb(h: int, s: int, v: int) -> tuple[int, int, int]:
    M = TFF * v
    m = M * (1 - s)
    z = (M - m) * (1 - abs(((h / 60) % 2) - 1))

    if 0 <= h < 60:
        r = M
        g = z + m
        b = m
    elif 60 <= h < 120:
        r = z + m
        g = M
        b = m
    elif 120 <= h < 180:
        r = m
        g = M
        b = z + m
    elif 180 <= h < 240:
        r = m
        g = z + m
        b = M
    elif 240 <= h < 300:
        r = z + m
        g = m
        b = M
    elif 300 <= h < 360:
        r = M
        g = m
        b = z + m

    return r, g, b


hsb2rgb = hsv2rgb


def hsv2hsl(h: int, s: int, v: int) -> tuple[int, int, int]:
    l = v * (1 - (s / 2))
    if l in (0, 1):
        s = 0
    else:
        s = (v - l) / min([l, 1 - l])
    return h, s, l


hsb2hsl = hsv2hsl


def hsv2cmyk(h: int, s: int, v: int) -> tuple[int, int, int, int]:
    r, g, b = hsv2rgb(h, s, l)
    return rgb2cmyk(r, g, b)


hsb2cmyk = hsv2cmyk


def cmyk2hex(c: int, m: int, y: int, k: int) -> str:
    r, g, b = cmyk2rgb(c, m, y, k)
    return rgb2hex(r, g, b)


def cmyk2rgb(c: int, m: int, y: int, k: int) -> tuple[int, int, int]:
    lbd = lambda value: TFF * (1 - (value / 100)) * (1 - (k / 100))
    r = lbd(c)
    g = lbd(m)
    b = lbd(y)
    return r, g, b


def cmyk2hsl(c: int, m: int, y: int, k: int) -> tuple[int, int, int]:
    r, g, b = cmyk2rgb(c, m, y, k)
    return rgb2hsl(r, g, b)


def cmyk2hsv(c: int, m: int, y: int, k: int) -> tuple[int, int, int, int]:
    r, g, b = cmyk2rgb(c, m, y, k)
    return rgb2hsv(r, g, b)


cmyk2hsb = cmyk2hsv


def rgb_tones_tints_shades(
    r: int, g: int, b: int, numbers: int
) -> list[tuple[int, int, int]]:
    ...


def array_values(size: int) -> list[float]:
    res = []
    i = 1 / size
    r = 0
    for _ in range(size):
        r += i
        res.append(r)
    return res


def value_array(value: int, array: list[int]):
    return [value * a for a in array]


def color_array(
    hex: str, size: int, bright: bool = False, saturation: bool = False
) -> list[str]:
    hs, col = (hex2hsv, hsv2hex) if bright else (hex2hsl, hsl2hex)

    h, s, w = hs(hex)
    array = array_values(size)

    arg = s if saturation else w

    values = value_array(arg, array)
    colors = []
    for value in values:
        args = (value, w) if saturation else (s, value)
        color = col(h, *args)
        colors.append(color)
    return colors


def saturation_array(hex: str, size: int, bright: bool = False) -> list[str]:
    return color_array(hex, size, bright, True)


def saturation_l_array(hex: str, size: int) -> list[str]:
    return saturation_array(hex, size)


def saturation_b_array(hex: str, size: int) -> list[str]:
    return saturation_array(hex, size, True)


def whiteness_array(hex: str, size: int, bright: bool = False) -> list[str]:
    return color_array(hex, size, bright)


def lightness_array(hex: str, size: int) -> list[str]:
    return whiteness_array(hex, size)


def brightness_array(hex: str, size: int) -> list[str]:
    return whiteness_array(hex, size, True)


def color_grid(hex: str, size: int, light: bool = False) -> list[list[str]]:
    assert size

    _row, _col = (
        (lightness_array, saturation_l_array)
        if light
        else (brightness_array, saturation_b_array)
    )

    grid = []
    first_col = _row(hex, size)
    first_col.reverse()

    for col in first_col:
        row = _col(col, size)
        grid.append(row)

    return grid


def color_l_grid(hex: str, size: int) -> list[list[str]]:
    return color_grid(hex, size, True)


def color_b_grid(hex: str, size: int) -> list[list[str]]:
    return color_grid(hex, size)
