#!/usr/bin/env python3


def parse(input_file):
    dots = set()
    instructions = list()
    with open(input_file, "r") as hand:
        read_instructions = False
        for line in hand:
            line = line.strip()
            if line == "":
                read_instructions = True
                continue
            if read_instructions:
                direction, breakpoint = line[len("fold along "):].split("=")
                instructions.append((direction, int(breakpoint)))
            else:
                dots.add(tuple(map(int, line.split(","))))
    return dots, instructions


def _print_board(dots):
    max_x = max(dots, key=lambda dot: dot[0])[0] + 1
    max_y = max(dots, key=lambda dot: dot[1])[1] + 1
    board = list()
    for _ in range(max_y):
        board.append([" "] * max_x)
    for x, y in dots:
        board[y][x] = "#"
    raw_board = list()
    for line in board:
        raw_board.append("".join(line))
    print("\n".join(raw_board))


def _fold_x(points, fold_point):
    new_points = set()
    for x, y in points:
        new_x = x if x < fold_point else 2 * fold_point - x
        new_points.add((new_x, y))
    return new_points


def _fold_y(points, fold_point):
    new_points = set()
    for x, y in points:
        new_y = y if y < fold_point else 2 * fold_point - y
        new_points.add((x, new_y))
    return new_points


def _fold(points, direction, fold_point):
    if direction == "x":
        new_points = _fold_x(points, fold_point)
    else:
        new_points = _fold_y(points, fold_point)
    return new_points


def solve1(dots, instructions):
    direction, fold_point = instructions[0]
    new_points = _fold(dots, direction, fold_point)
    return len(new_points)


def solve2(dots, instructions):
    for direction, fold_point in instructions:
        dots = _fold(dots, direction, fold_point)
    return dots


if __name__ == "__main__":
    dots, instructions = parse("input")
    solution1 = solve1(dots, instructions)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(dots, instructions)
    print("Solution 2:")
    _print_board(solution2)
