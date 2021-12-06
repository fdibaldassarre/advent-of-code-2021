#!/usr/bin/env python3


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            line = line.strip()
            start, end = line.split(" -> ")
            start_x, start_y = map(int, start.split(","))
            end_x, end_y = map(int, end.split(","))
            data.append(((start_x, start_y), (end_x, end_y)))
    return data


def create_grid(data):
    max_x, max_y = -1, -1
    for line in data:
        start, end = line
        start_x, start_y = start
        end_x, end_y = end
        max_x = max(max_x, start_x, end_x)
        max_y = max(max_y, start_y, end_y)
    grid = list()
    for x in range(max_x + 1):
        grid.append([0] * (max_y + 1))
    return grid


def draw(grid, data, only_vert_and_horiz=True):
    for line in data:
        start, end = line
        start_x, start_y = start
        end_x, end_y = end
        if only_vert_and_horiz and start_x != end_x and start_y != end_y:
            continue
        dx = 1 if end_x - start_x > 0 else -1 if end_x - start_x < 0 else 0
        dy = 1 if end_y - start_y > 0 else -1 if end_y - start_y < 0 else 0
        d = max(abs(end_x - start_x), abs(end_y - start_y))
        for i in range(d + 1):
            grid[start_x + dx * i][start_y + dy * i] += 1


def count_intersections(grid):
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] > 1:
                count += 1
    return count


def solve1(data):
    grid = create_grid(data)
    draw(grid, data, only_vert_and_horiz=True)
    return count_intersections(grid)


def solve2(data):
    grid = create_grid(data)
    draw(grid, data, only_vert_and_horiz=False)
    return count_intersections(grid)


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
