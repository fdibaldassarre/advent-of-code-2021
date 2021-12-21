#!/usr/bin/env python3


def parse(input_file):
    with open(input_file, "r") as hand:
        position1 = int(hand.readline().strip()[len("Player 1 starting position: "):])
        position2 = int(hand.readline().strip()[len("Player 2 starting position: "):])
    return position1, position2


def roll_deterministic():
    i = 0
    while True:
        yield i + 1
        i = (i + 1) % 10


def get_possible_dice_results():
    results = dict()
    for i in range(3):
        for j in range(3):
            for z in range(3):
                res = i + j + z + 3
                if res not in results:
                    results[res] = 0
                results[res] += 1
    return results


def solve1(initial_positions):
    scores = [0, 0]
    player = 0
    dice = roll_deterministic()
    n_rolls = 0
    positions = [initial_positions[0], initial_positions[1]]
    while max(scores) < 1000:
        for _ in range(3):
            positions[player] += next(dice)
        positions[player] = positions[player] % 10
        scores[player] += _get_score(positions[player])
        player = (player + 1) % 2
        n_rolls += 3
    return n_rolls * min(scores)


def _get_score(position):
    return (position - 1) % 10 + 1


def solve2(initial_positions):
    dice = get_possible_dice_results()
    cache = dict()

    def split_universes(position1, position2, score1=0, score2=0):
        if (position1, position2, score1, score2) in cache:
            return cache[(position1, position2, score1, score2)]
        if score1 >= 21:
            return 1, 0
        elif score2 >= 21:
            return 0, 1
        # Throw the dice
        universes = [0, 0]
        for value1, times1 in dice.items():
            new_pos1 = (position1 + value1) % 10
            new_score1 = score1 + _get_score(new_pos1)
            if new_score1 >= 21:
                universes[0] += times1
                continue
            for value2, times2 in dice.items():
                new_pos2 = (position2 + value2) % 10
                new_score2 = score2 + _get_score(new_pos2)
                victories = split_universes(new_pos1, new_pos2, new_score1, new_score2)
                universes[0] += (times1 * times2) * victories[0]
                universes[1] += (times1 * times2) * victories[1]
        cache[(position1, position2, score1, score2)] = tuple(universes)
        return cache[(position1, position2, score1, score2)]
    universes = split_universes(*initial_positions)
    return max(universes)


if __name__ == "__main__":
    positions = parse("input")
    solution1 = solve1(positions)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(positions)
    print("Solution 2: %d" % solution2)
