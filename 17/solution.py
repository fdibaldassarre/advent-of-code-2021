#!/usr/bin/env python3


def parse(input_file):
    with open(input_file, "r") as hand:
        data = hand.readline().strip()[len("target area: "):]
        x_raw, y_raw = data.split(", ")
        x_min, x_max = tuple(map(int, x_raw[2:].split("..")))
        y_min, y_max = tuple(map(int, y_raw[2:].split("..")))
    return (x_min, x_max), (y_min, y_max)


def compute_trajectory(vx, vy):
    dvx, dvy = vx, vy
    x, y = 0, 0
    while True:
        x = x + dvx
        y = y + dvy
        dvx = max(0, dvx - 1)
        dvy -= 1
        yield (x, y), (dvx, dvy)


def solve(x_range, y_range):
    max_y = 0
    tot_valid = 0
    for vx in range(1, x_range[1] + 1):
        for vy in range(y_range[0], 1000):
            is_valid = False
            max_y_current = 0
            for point, speed in compute_trajectory(vx, vy):
                x, y = point
                dx, _ = speed
                max_y_current = max(max_y_current, y)
                if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                    is_valid = True
                    break
                if dx == 0:
                    if x < x_range[0] or x > x_range[1] or y < y_range[0]:
                        break
            if is_valid:
                tot_valid += 1
                max_y = max(max_y, max_y_current)
    return max_y, tot_valid


if __name__ == "__main__":
    data = parse("input")
    solution1, solution2 = solve(*data)
    print("Solution 1: %d" % solution1)
    print("Solution 2: %d" % solution2)
