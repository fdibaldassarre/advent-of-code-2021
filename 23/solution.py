#!/usr/bin/env python3

import heapq


ROOMS = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

ENERGY = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        hand.readline()
        hand.readline()
        for y in range(2):
            line = hand.readline()[1:-2]
            for x, ch in enumerate(line):
                if ch != " " and ch != "#":
                    data.append((ch, x, 1 + y))
    data.sort()
    return tuple(data)


class Position:
    def __init__(self, pods, depth=2):
        self.depth = depth
        self.pods = pods
        self.rooms = dict()
        for pod_type, x, y in pods:
            self.rooms[(x, y)] = pod_type

    def isOccupied(self, cell):
        return cell in self.rooms

    def getPodTypeAt(self, cell):
        return None if cell not in self.rooms else self.rooms[cell]

    def movePodTo(self, idx, cell):
        pod_type, pod_x, pod_y = self.pods[idx]
        new_position = list(self.pods)
        new_position[idx] = (pod_type, cell[0], cell[1])
        new_position.sort()
        energy = get_energy(pod_type, (pod_x, pod_y), cell)
        return energy, tuple(new_position)

    def toString(self):
        value = list()
        value.append("#" * 13)
        hallway = [" "] * 11
        for x in range(11):
            if (x, 0) in self.rooms:
                hallway[x] = self.rooms[(x, 0)]
        value.append("#" + "".join(hallway) + "#")
        for dy in range(self.depth):
            rooms = [" "] * 11
            for x in range(11):
                y = 1 + dy
                if (x, y) in self.rooms:
                    rooms[x] = self.rooms[(x, y)]
            value.append("#" + "".join(rooms) + "#")
        value.append("#" * 13)
        return "\n".join(value)


def isComplete(position):
    for pod, x, _ in position:
        if ROOMS[pod] != x:
            return False
    return True


def are_same_cell(a, b):
    return a[0] == b[0] and a[1] == b[1]


def canMoveTo(source, target, position):
    sx, sy = source
    tx, ty = target
    # Go to the corridor
    for i in range(sy, 0, -1):
        if position.isOccupied((sx, i - 1)):
            return False
    # Move on the corridor
    dx = 1 if tx > sx else -1
    for x in range(sx, tx, dx):
        if position.isOccupied((x + dx, 0)):
            return False
    # Move in the room
    for i in range(ty):
        if position.isOccupied((tx, i + 1)):
            return False
    return True


def get_energy(pod_type, source, target):
    sx, sy = source
    tx, ty = target
    if sx == tx:
        d = abs(sy - ty)
    else:
        d = abs(sy) + abs(ty) + abs(sx - tx)
    return ENERGY[pod_type] * d


def isPodTypeComplete(position, pod_type):
    x = ROOMS[pod_type]
    for level in position.depth:
        pod = position.getPodTypeAt((x, level + 1))
        if pod != pod_type:
            return False
    return True


def podIsInCorrectPosition(position, pod_type, pod_cell):
    podx, pody = pod_cell
    if ROOMS[pod_type] != podx:
        return False
    for y in range(pody, position.depth):
        if position.getPodTypeAt((podx, y + 1)) != pod_type:
            return False
    return True


def roomsContainsOnlyCorrectPods(position, pod_type):
    x = ROOMS[pod_type]
    for y in range(position.depth):
        room_mate_type = position.getPodTypeAt((x, y + 1))
        if room_mate_type is not None and room_mate_type != pod_type:
            return False
    return True


def getTargetCell(position, pod_type):
    x = ROOMS[pod_type]
    for y in range(position.depth, 0, -1):
        if position.getPodTypeAt((x, y)) is None:
            return x, y


def movePod(idx, position):
    pod_type, podx, pody = position.pods[idx]
    pod_cell = (podx, pody)
    if podIsInCorrectPosition(position, pod_type, pod_cell):
        return
    if pod_cell[1] == 0:
        # In hallway, can move only to the target room
        target_cell = getTargetCell(position, pod_type)
        if target_cell is not None and roomsContainsOnlyCorrectPods(position, pod_type) and canMoveTo(pod_cell, target_cell, position):
            yield position.movePodTo(idx, target_cell)
    else:
        # In cell
        # Move to hallway
        for x in range(11):
            if x in {2,4,6,8}:
                continue
            if canMoveTo(pod_cell, (x, 0), position):
                yield position.movePodTo(idx, (x, 0))


def getNextPositions(position):
    for i, pod in enumerate(position.pods):
        for denergy, new_position in movePod(i, position):
            yield denergy, new_position


def solve1(initial_position, depth=2):
    positions = list()
    explored = set()
    heapq.heapify(positions)
    heapq.heappush(positions, (0, initial_position))
    min_energy = None
    while len(positions) > 0:
        energy, position = heapq.heappop(positions)
        if position in explored:
            continue
        explored.add(position)
        if isComplete(position):
            min_energy = energy
            break
        position = Position(position, depth=depth)
        for denergy, new_position in getNextPositions(position):
            heapq.heappush(positions, (energy + denergy, new_position))
    return min_energy


def enhance(initial_position):
    new_positions = list()
    for pod_type, x, y in initial_position:
        if y == 2:
            y = 4
        new_positions.append((pod_type, x, y))
    new_positions.append(('D', 2, 2))
    new_positions.append(('D', 2, 3))
    new_positions.append(('C', 4, 2))
    new_positions.append(('B', 4, 3))
    new_positions.append(('B', 6, 2))
    new_positions.append(('A', 6, 3))
    new_positions.append(('A', 8, 2))
    new_positions.append(('C', 8, 3))
    new_positions.sort()
    return tuple(new_positions)


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    data = enhance(data)
    solution2 = solve1(data, depth=4)
    print("Solution 2: %d" % solution2)
