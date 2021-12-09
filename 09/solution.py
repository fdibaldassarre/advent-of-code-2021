#!/usr/bin/env python3
import heapq


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            line = line.strip()
            data.append(list(map(int, line)))
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


def get_lowpoints(heatmap):
    N, M = len(heatmap), len(heatmap[0])
    for x, line in enumerate(data):
        for y, value in enumerate(line):
            is_lowpoint = True
            for nx, ny in get_neighbours(x, y, N, M):
                if value >= heatmap[nx][ny]:
                    is_lowpoint = False
                    break
            if is_lowpoint:
                yield x, y


def solve1(heatmap):
    total = 0
    for x, y in get_lowpoints(heatmap):
        total += heatmap[x][y] + 1
    return total


def solve2(heatmap):
    top_basins = [0, 0, 0]
    heapq.heapify(top_basins)
    N, M = len(heatmap), len(heatmap[0])
    for lx, ly in get_lowpoints(heatmap):
        basin = {(lx, ly)}
        border = {(lx, ly)}
        while len(border) > 0:
            new_border = set()
            # Expand the basin
            for x, y in border:
                for nx, ny in get_neighbours(x, y, N, M):
                    if heatmap[nx][ny] == 9 or (nx, ny) in basin:
                        continue
                    new_border.add((nx, ny))
                    basin.add((nx, ny))
            border = new_border
        # Add the basin to the heap
        heapq.heappush(top_basins, len(basin))
        heapq.heappop(top_basins)
    return top_basins[0] * top_basins[1] * top_basins[2]


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
