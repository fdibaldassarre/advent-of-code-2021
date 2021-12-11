#!/usr/bin/env python3

import copy


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            data.append(list(map(int, line.strip())))
    return data


def get_all_neighbours(x, y):
    yield x - 1, y + 1
    yield x - 1, y
    yield x - 1, y - 1
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x + 1, y
    yield x + 1, y - 1


def get_valid_neighbours(x, y):
    for nx, ny in get_all_neighbours(x, y):
        if 0 <= nx < 10 and 0 <= ny < 10:
            yield nx, ny


def perform_step(status):
    n_flashes = 0
    # Flash once
    flashing = set()
    for x in range(10):
        for y in range(10):
            status[x][y] += 1
            if status[x][y] == 10:
                flashing.add((x, y))
    while len(flashing) > 0:
        fx, fy = flashing.pop()
        for nx, ny in get_valid_neighbours(fx, fy):
            if status[nx][ny] == 10:
                # Already flashed
                continue
            status[nx][ny] += 1
            if status[nx][ny] == 10:
                flashing.add((nx, ny))
    # Reset the energy to 0
    for x in range(10):
        for y in range(10):
            if status[x][y] == 10:
                n_flashes += 1
                status[x][y] = 0
    return n_flashes


def solve1(data):
    status = copy.deepcopy(data)
    tot_flashes = 0
    for steps in range(100):
        step_flashes = perform_step(status)
        tot_flashes += step_flashes
    return tot_flashes


def solve2(data):
    status = copy.deepcopy(data)
    current_step = 0
    while True:
        current_step += 1
        step_flashes = perform_step(status)
        if step_flashes == 100:
            break
    return current_step


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
