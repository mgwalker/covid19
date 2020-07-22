from math import fabs, floor
import sys

__color_bins = [
    # "rgb(128, 192, 128)",
    # "rgb(128, 255, 128)",
    "rgb(0, 255, 0)",
    "rgb(255, 255, 0)",
    "rgb(255, 128, 0)",
    "rgb(255,0,0)",
]


def __get_bins(data, key, type):
    max_value = 0
    min_value = sys.maxsize

    for locale in data.values():
        value = locale[key][type][-1]
        if value < min_value:
            min_value = max(value, 0)
        if value > max_value:
            max_value = min(value, 10000)

    min_value = min_value + (max_value - min_value) * -0.3
    # max_value = max_value * 0.8

    bins = len(__color_bins)
    step = (max_value - min_value) / bins
    ceils = []
    for v in range(bins):
        ceils.append(min_value + (v + 1) * step)
    print(ceils)

    def get_color(value):
        if value == 0:
            return "rgb(128, 192, 128)"

        for i, ceil in enumerate(ceils):
            if value < ceil:
                return __color_bins[i]
        return __color_bins[-1]

    return get_color


def draw_county_map(counties, inpath, outpath):
    svg = ""
    with open(inpath) as svgfile:
        svg = svgfile.read()

    key = "recent"
    type = "cases"

    bins = __get_bins(counties, key, type)
    for locale in counties.values():
        fips = locale["fips"]
        # color = __color_bins[bins(locale[key][type][-1])]
        color = bins(locale[key][type][-1])
        svg = svg.replace(f'id="FIPS_{fips}"', f'id="FIPS_{fips}" fill="{color}"')

    with open(outpath, "w") as out:
        out.write(svg)
