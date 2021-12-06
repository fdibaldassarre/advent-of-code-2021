#!/usr/bin/env python3

import math


def parse(input_file):
    data = None
    with open(input_file, "r") as hand:
        for line in hand:
            data = list(map(int, line.strip().split(",")))
    return data


def get_total(data, days):
    dp = dict()

    def get_lanternfishes_with_wait_time(k, ages):
        if (k, ages) in dp:
            return dp[(k, ages)]
        if k > ages:
            return 1
        n = int(math.ceil((ages - k) / 7))
        result = 1
        for i in range(n):
            wt = k + i * 7 + 9
            result += get_lanternfishes_with_wait_time(wt, ages)
        dp[(k, ages)] = result
        return dp[(k, ages)]

    total = 0
    for wait_time in data:
        total += get_lanternfishes_with_wait_time(wait_time, days)
    return total


def solve1(data):
    return get_total(data, days=80)


def solve2(data):
    return get_total(data, days=256)


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
