#!/usr/bin/env python3


def parse(input_file):
    steps = list()
    with open(input_file, "r") as hand:
        for line in hand:
            line = line.strip()
            turn_on = True if line[:2] == "on" else False
            coordinates = line.split(" ")[1].split(",")
            cube = list()
            for coordinate in coordinates:
                start, end = tuple(map(int, coordinate[2:].split("..")))
                cube.append((start, end))
            steps.append((turn_on, Cube(cube)))
    return steps


class Cube:
    def __init__(self, ranges):
        self.ranges = ranges
        self.oversized = False
        for s in ranges:
            if max(map(abs, s)) > 50:
                self.oversized = True
                break

    def getVolume(self):
        tot = 1
        for i in range(3):
            tot *= (self.ranges[i][1] - self.ranges[i][0] + 1)
        return tot

    def intersection(self, other):
        ranges = [None] * 3
        for i in range(3):
            ranges[i] = (max(self.ranges[i][0], other.ranges[i][0]), min(self.ranges[i][1], other.ranges[i][1]))
            if ranges[i][0] > ranges[i][1]:
                return None
        return Cube(ranges)


def solve(steps, skip=True):

    def turn_map(i):
        if i == 1:
            return -1
        elif i == 0:
            return 1
        else:
            return 1

    previous = list()
    for i in range(len(steps)):
        turn_on, cube = steps[i]
        if skip and cube.oversized:
            continue
        new_steps = list()
        if turn_on:
            new_steps.append((1, cube))
        for action, other in previous:
            inter = cube.intersection(other)
            if inter is not None:
                if turn_on:
                    inter_action = turn_map(action)
                else:
                    inter_action = -1 * action
                if not turn_on and inter_action == 0:
                    continue
                new_steps.append((inter_action, inter))
        previous.extend(new_steps)
    tot = 0
    for action, cube in previous:
        tot += action * cube.getVolume()
    return tot


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve(data, skip=True)
    print("Solution 1: %d" % solution1)
    solution2 = solve(data, skip=False)
    print("Solution 2: %d" % solution2)
