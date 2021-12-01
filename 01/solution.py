import collections


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            data.append(int(line))
    return data


def solve1(data):
    increased = 0
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            increased += 1
    return increased


def solve2(data):
    window = collections.deque([data[0], data[1], data[2]])
    current_depth = sum(window)
    increased = 0
    for i in range(3, len(data)):
        previous_depth = current_depth
        depth = data[i]
        current_depth = current_depth - window.popleft() + depth
        window.append(depth)
        if current_depth > previous_depth:
            increased += 1
    if sum(window) > current_depth:
        increased += 1
    return increased


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
