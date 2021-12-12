#!/usr/bin/env python3


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            start, end = line.strip().split("-")
            data.append((start, end))
    return data


def build_connection_paths(connections):
    # Build point to possible directions
    paths = dict()
    for start, end in connections:
        if start not in paths:
            paths[start] = set()
        paths[start].add(end)
        if end not in paths:
            paths[end] = set()
        paths[end].add(start)
    return paths


def navigate(paths, allow_small_twice=False):
    visited = set()
    def _navigate(point, visited_small_twice=False):
        if point == "end":
            return 1
        is_duplicated = False
        if point in visited:
            if point == "start" or visited_small_twice:
                return 0
            else:
                visited_small_twice = True
                is_duplicated = True
        if point.islower() and not is_duplicated:
            visited.add(point)
        total = 0
        for target in paths[point]:
            total += _navigate(target, visited_small_twice=visited_small_twice)
        if point.islower() and not is_duplicated:
            visited.remove(point)
        return total
    return _navigate("start", visited_small_twice=not allow_small_twice)


def solve1(paths):
    return navigate(paths)


def solve2(paths):
    return navigate(paths, allow_small_twice=True)


if __name__ == "__main__":
    data = parse("input")
    paths = build_connection_paths(data)
    solution1 = solve1(paths)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(paths)
    print("Solution 2: %d" % solution2)
