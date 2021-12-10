#!/usr/bin/env python3
import collections


MATCHING_BRACKETS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            data.append(line.strip())
    return data


def find_errors(lines):
    illegal_characters = {')': 0, ']': 0, '}': 0, '>': 0}
    missing_brackets = list()
    for line in lines:
        brackets = collections.deque()
        is_corrupted = False
        for ch in line:
            if ch in MATCHING_BRACKETS.keys():
                brackets.append(ch)
            else:
                opening = brackets.pop()
                if ch != MATCHING_BRACKETS[opening]:
                    # Corrupted
                    is_corrupted = True
                    illegal_characters[ch] += 1
                    break
        if not is_corrupted and len(brackets) > 0:
            brackets.reverse()
            completion = list()
            for ch in brackets:
                completion.append(MATCHING_BRACKETS[ch])
            missing_brackets.append(completion)
    return illegal_characters, missing_brackets


def solve1(illegal_characters):
    return 3 * illegal_characters[')'] + 57 * illegal_characters[']'] + 1197 * illegal_characters['}'] + \
           25137 * illegal_characters['>']


def solve2(missing_brackets):
    scores = {')': 1, ']': 2, '}': 3, '>': 4}
    all_scores = list()
    for missing in missing_brackets:
        score = 0
        for ch in missing:
            score = 5 * score + scores[ch]
        all_scores.append(score)
    all_scores.sort()
    return all_scores[len(all_scores) // 2]


if __name__ == "__main__":
    data = parse("input")
    illegal_characters, missing_brackets = find_errors(data)
    solution1 = solve1(illegal_characters)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(missing_brackets)
    print("Solution 2: %d" % solution2)
