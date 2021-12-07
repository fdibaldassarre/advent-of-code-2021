#!/usr/bin/env python3

import collections


def parse(input_file):
    with open(input_file, "r") as hand:
        data = list(map(int, hand.readline().strip().split(",")))
    return data


def solve(positions, increase_depends_distance=False):
    current = 0
    right_crabs = 0
    left_crabs = 0
    crab_locations = collections.defaultdict(int)
    for position in positions:
        if increase_depends_distance:
            current += (position * (position + 1)) // 2
        else:
            current += position
        if position == 0:
            left_crabs += 1
        else:
            right_crabs += 1
        crab_locations[position] += 1
    M = max(positions)
    min_carburant = current
    for position in range(1, M + 1):
        if increase_depends_distance:
            current = 0
            for original in positions:
                delta = abs(original - position)
                current += (delta * (delta+1)) // 2
        else:
            current = current + left_crabs - right_crabs
        min_carburant = min(min_carburant, current)
        left_crabs += crab_locations[position]
        right_crabs -= crab_locations[position]
    return min_carburant


def solve1(positions):
    return solve(positions, increase_depends_distance=False)


def solve2(positions):
    return solve(positions, increase_depends_distance=True)


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
