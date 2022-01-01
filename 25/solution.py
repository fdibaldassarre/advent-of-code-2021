#!/usr/bin/env python3

SOUTH_FACING = "v"
EAST_FACING = ">"
EMPTY_SPACE = "."

class Map:
    def __init__(self, size, data):
        self.size = size
        self.data = data
        self.east_facing = set()
        self.south_facing = set()
        for pos, ch in data.items():
            if ch == SOUTH_FACING:
                self.south_facing.add(pos)
            elif ch == EAST_FACING:
                self.east_facing.add(pos)

    def _is_empty(self, x, y):
        return self.data[(x, y)] == EMPTY_SPACE

    def _get_cucumbers_that_could_move_east(self):
        cucumbers_that_could_move_east = set()
        for cucumber in self.east_facing:
            x, y = cucumber
            x = (x + 1) % self.size[0]
            if self._is_empty(x, y):
                cucumbers_that_could_move_east.add((cucumber, (x,y)))
        return cucumbers_that_could_move_east

    def _get_cucumbers_that_could_move_south(self):
        cucumbers_that_could_move_south = set()
        for cucumber in self.south_facing:
            x, y = cucumber
            y = (y + 1) % self.size[1]
            if self._is_empty(x, y):
                cucumbers_that_could_move_south.add((cucumber, (x,y)))
        return cucumbers_that_could_move_south

    def update(self):
        cucumbers_that_could_move_east = self._get_cucumbers_that_could_move_east()
        moved = 0
        for cucumber, pos in cucumbers_that_could_move_east:
            self.data[pos] = EAST_FACING
            self.data[cucumber] = EMPTY_SPACE
            self.east_facing.remove(cucumber)
            self.east_facing.add(pos)
            moved += 1
        cucumbers_that_could_move_south = self._get_cucumbers_that_could_move_south()
        for cucumber, pos in cucumbers_that_could_move_south:
            self.data[pos] = SOUTH_FACING
            self.data[cucumber] = EMPTY_SPACE
            self.south_facing.remove(cucumber)
            self.south_facing.add(pos)
            moved += 1
        return moved != 0

    def print(self):
        grid = list()
        for y in range(self.size[1]):
            line = [EMPTY_SPACE] * self.size[0]
            grid.append(line)
        for x, y in self.south_facing:
            grid[y][x] = SOUTH_FACING
        for x, y in self.east_facing:
            grid[y][x] = EAST_FACING
        for y in range(self.size[1]):
            print("".join(grid[y]))


def parse(input_file):
    data = dict()
    with open(input_file, "r") as hand:
        for y, line in enumerate(hand):
            line = line.strip()
            M = len(line)
            for x, ch in enumerate(line):
                data[(x, y)] = ch
            N = y + 1
    return (M, N), data


def solve1(data):
    map = Map(*data)
    moved = True
    steps = 0
    while moved:
        moved = map.update()
        steps += 1
    return steps


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
