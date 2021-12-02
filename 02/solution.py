#!/usr/bin/env python3


MOVE_FORWARD = "forward"
MOVE_DOWN = "down"
MOVE_UP = "up"

def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            move_type, value = line.split(" ")
            data.append((move_type, int(value)))
    return data


def solve1(data):
    x, y = 0, 0
    for move in data:
        move_type, value = move
        if move_type == MOVE_FORWARD:
            x += value
        elif move_type == MOVE_DOWN:
            y += value
        else:
            y -= value
    return x * y


def solve2(data):
    x, y, aim = 0, 0, 0
    for move in data:
        move_type, value = move
        if move_type == MOVE_FORWARD:
            x += value
            y += value * aim
        elif move_type == MOVE_DOWN:
            aim += value
        else:
            aim -= value
    return x * y


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
