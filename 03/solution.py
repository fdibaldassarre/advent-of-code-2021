#!/usr/bin/env python3


def parse(input_file):
    data = list()
    N = 0
    with open(input_file, "r") as hand:
        for line in hand:
            if N == 0:
                N = len(line.strip())
            value = 0
            for el in line.strip():
                value = 2 * value + int(el)
            data.append(value)
    return data, N


def solve1(data, N):
    gamma = 0
    epsilon = 0
    for i in range(N, 0, -1):
        tot = 0
        for value in data:
            if value >> (i - 1) & 1 == 1:
                tot += 1
        if 2 * tot >= len(data):
            gamma = 2 * gamma + 1
            epsilon = 2 * epsilon
        else:
            gamma = 2 * gamma
            epsilon = 2 * epsilon + 1
    return gamma * epsilon


def filter_candidates(candidates, i, most_common=True):
    tot_ones = 0
    for candidate in candidates:
        if candidate >> (i - 1) & 1 == 1:
            tot_ones += 1
    if 2 * tot_ones >= len(candidates):
        target = 1
    else:
        target = 0
    if not most_common and tot_ones < len(candidates):
        target = 1 - target
    new_candidates = set()
    for candidate in candidates:
        if candidate >> (i - 1) & 1 == target:
            new_candidates.add(candidate)
    return new_candidates


def solve2(data, N):
    candidatates_oxygen = set(data)
    candidates_co2 = set(data)
    for i in range(N, 0, -1):
        if len(candidatates_oxygen) > 1:
            candidatates_oxygen = filter_candidates(candidatates_oxygen, i, most_common=True)
        if len(candidates_co2) > 1:
            candidates_co2 = filter_candidates(candidates_co2, i, most_common=False)
    co_scrubber = candidatates_oxygen.pop()
    oxygen_rating = candidates_co2.pop()
    return co_scrubber * oxygen_rating


if __name__ == "__main__":
    data, N = parse("input")
    solution1 = solve1(data, N)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data, N)
    print("Solution 2: %d" % solution2)
