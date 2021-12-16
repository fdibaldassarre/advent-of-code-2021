#!/usr/bin/env python3

import heapq


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            data.append(list(map(int, line.strip())))
    return data


def get_neighbours(x, y, N, M):
    if x > 0:
        yield x - 1, y
    if x < N - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < M - 1:
        yield x, y + 1


def explore(risk_map, size_multiplier=1):
    original_N, original_M = len(risk_map), len(risk_map[0])
    N = original_N * size_multiplier
    M = original_M * size_multiplier

    total_risk = list()
    for _ in range(N):
        total_risk.append([-1] * M)
    total_risk[0][0] = 0
    border = [(0, 0, 0)]
    heapq.heapify(border)

    def _get_risk(a, b):
        if size_multiplier == 1:
            return risk_map[a][b]
        dx = a // original_N
        dy = b // original_M
        risk = risk_map[a % original_N][b % original_M] + dx + dy
        if risk < 10:
            return risk
        else:
            return risk % 10 + 1

    def _navigate(x, y):
        for nx, ny in get_neighbours(x, y, N, M):
            if total_risk[nx][ny] == -1:
                total_risk[nx][ny] = total_risk[x][y] + _get_risk(nx, ny)
                heapq.heappush(border, (total_risk[nx][ny], nx, ny))

    while len(border) > 0:
        _, x, y = heapq.heappop(border)
        if x == N - 1 and y == M - 1:
            break
        _navigate(x, y)

    return total_risk[N - 1][M - 1]


def solve1(risk_map):
    return explore(risk_map)


def solve2(risk_map):
    return explore(risk_map, size_multiplier=5)


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
