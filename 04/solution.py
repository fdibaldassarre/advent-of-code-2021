#!/usr/bin/env python3


def parse(input_file):
    boards = list()
    with open(input_file, "r") as hand:
        current_board = None
        extracted = list(map(int, hand.readline().strip().split(",")))
        for line in hand:
            line = line.strip();
            if line == "":
                if current_board is not None:
                    boards.append(current_board)
                current_board = list()
            else:
                values = list(map(int, filter(lambda el: el != '', line.split(" "))))
                current_board.append(values)
    boards.append(current_board)
    return extracted, boards


def play(data, stop_at_first=True):
    extracted, raw_boards = data
    values_to_boards = dict()
    unmarked_values = dict()
    for board_id, board in enumerate(raw_boards):
        unmarked_values[board_id] = [None] * 5
        for i in range(5):
            unmarked_values[board_id][i] = [1] * 5
        for i in range(5):
            for j in range(5):
                value = board[i][j]
                if value not in values_to_boards:
                    values_to_boards[value] = list()
                values_to_boards[value].append((board_id, i, j))
    board_column_to_victory = dict()
    board_row_to_victory = dict()
    winning_number = None
    winning_boards = list()
    boards_that_won = set()
    for value in extracted:
        if value not in values_to_boards:
            continue
        for marked in values_to_boards[value]:
            board_id, i, j = marked
            if board_id in boards_that_won:
                continue
            unmarked_values[board_id][i][j] = 0
            if board_id not in board_column_to_victory:
                board_column_to_victory[board_id] = [0] * 5
            board_column_to_victory[board_id][i] += 1
            if board_id not in board_row_to_victory:
                board_row_to_victory[board_id] = [0] * 5
            board_row_to_victory[board_id][j] += 1
            if board_column_to_victory[board_id][i] == 5 or board_row_to_victory[board_id][j] == 5:
                # We won
                winning_number = value
                winning_boards.append(board_id)
                boards_that_won.add(board_id)
        if winning_number is not None:
            if stop_at_first:
                break
            elif len(winning_boards) == len(raw_boards):
                break
            else:
                winning_number = None
    best_score = -1
    winning_board = winning_boards[-1]
    score = 0
    for i in range(5):
        for j in range(5):
            score += unmarked_values[winning_board][i][j] * raw_boards[winning_board][i][j]
    score *= winning_number
    best_score = max(best_score, score)
    return best_score


def solve1(data):
    return play(data, stop_at_first=True)


def solve2(data):
    return play(data, stop_at_first=False)


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
