#!/usr/bin/env python3

import sys


def parse(input_file):
    with open(input_file, "r") as hand:
        convolution = hand.readline().strip()
        hand.readline()
        image = list()
        for line in hand:
            image.append(line.strip())
    return convolution, image


class Region:
    def __init__(self, x_region, y_region):
        self.x_region = list(x_region)
        self.y_region = list(y_region)

    def pad(self, padding):
        new_x_region = (self.x_region[0] - padding, self.x_region[1] + padding)
        new_y_region = (self.y_region[0] - padding, self.y_region[1] + padding)
        return Region(new_x_region, new_y_region)

    def update(self, x, y):
        self.x_region[0] = min(self.x_region[0], x)
        self.x_region[1] = max(self.x_region[1], x + 1)
        self.y_region[0] = min(self.y_region[0], y)
        self.y_region[1] = max(self.y_region[1], y + 1)

    def explore(self):
        for x in range(*self.x_region):
            for y in range(*self.y_region):
                yield x, y

    def contains(self, x, y):
        if x < self.x_region[0] or x >= self.x_region[1]:
            return False
        if y < self.y_region[0] or y >= self.y_region[1]:
            return False
        return True


class Image:
    def __init__(self, background=0):
        self.points = set()
        self.region = Region((0, 0), (0, 0))
        self.background = background

    def getRegion(self):
        return self.region

    def parse(self, image_raw):
        for i, raw_line in enumerate(image_raw):
            for j in range(len(raw_line)):
                if raw_line[j] == "#":
                    self.points.add((i, j))
        self.region = Region((0, len(image_raw)), (0, len(image_raw[0])))

    def getPoint(self, x, y):
        if (x, y) in self.points:
            return 1
        if not self.region.contains(x, y):
            return self.background
        return 0

    def addPoint(self, x, y):
        self.points.add((x, y))
        self.region.update(x, y)


def _to_binary(value):
    result = 0
    for ch in value:
        result = 2 * result + ch
    return result


class Convolution:
    def __init__(self):
        self.conv = None

    def parse(self, conv):
        self.conv = list()
        for i, value in enumerate(conv):
            self.conv.append(1 if value == "#" else 0)

    def _apply_at(self, image, x, y):
        value = list()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                value.append(image.getPoint(x + dx, y + dy))
        return self.conv[_to_binary(value)]

    def apply(self, image):
        new_background = self.conv[_to_binary([image.background] * 9)]  # Either 0 or 1
        new_image = Image(new_background)
        region = image.getRegion().pad(3)
        for x, y in region.explore():
            value = self._apply_at(image, x, y)
            if value == 1:
                new_image.addPoint(x, y)
        return new_image


def print_image(image):
    region = image.getRegion()
    x_prev = None
    print("-----------")
    for x, y in region.explore():
        if x != x_prev and x_prev is not None:
            sys.stdout.write("\n")
        if image.getPoint(x, y) == 1:
            sys.stdout.write("#")
        else:
            sys.stdout.write(" ")
        x_prev = x
    sys.stdout.write("\n")
    print("-----------")
    sys.stdout.flush()


def convolve(data, times):
    convolution = Convolution()
    convolution.parse(data[0])
    image = Image()
    image.parse(data[1])
    for _ in range(times):
        image = convolution.apply(image)
    return len(image.points)


def solve1(data):
    return convolve(data, times=2)


def solve2(data):
    return convolve(data, times=50)


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
