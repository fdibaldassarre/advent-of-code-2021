#!/usr/bin/env python3

import collections


def parse(input_file):
    pair_insertions = dict()
    with open(input_file, "r") as hand:
        start = hand.readline().strip()
        hand.readline()  # Skip the empty line
        for line in hand:
            source, target = line.strip().split(" -> ")
            pair_insertions[tuple(source)] = target
    return start, pair_insertions


def _compute_value(start, pair_insertions, iter_size=10):
    current = collections.deque(start)
    for _ in range(iter_size):
        result = collections.deque()
        prev = None
        for ch in current:
            if prev is not None:
                result.append(prev)
                key_pair = (prev, ch)
                if key_pair in pair_insertions:
                    generated = pair_insertions[key_pair]
                    result.append(generated)
            prev = ch
        result.append(prev)
        current = result
    return current

def _compute_result(start, pair_insertions, iter_size=10):
    current = _compute_value(start, pair_insertions, iter_size=iter_size)
    # Create counter
    counter = dict()
    for ch in current:
        if ch not in counter:
            counter[ch] = 0
        counter[ch] += 1
    return counter

def solve1(start, pair_insertions):
    values = _compute_result(start, pair_insertions, iter_size=10)
    counter = collections.Counter(values)
    _, most_common_count = counter.most_common(1)[0]
    _, least_common_count = counter.most_common()[-1]
    return most_common_count - least_common_count


def solve2(start, pair_insertions):
    cache_dict = dict()

    def _compute_pair(a, b, iter_count=1):
        if (a, b, iter_count) in cache_dict:
            return cache_dict[(a, b, iter_count)]
        if iter_count == 4:
            cache_dict[(a, b, iter_count)] = _compute_result(a + b, pair_insertions, iter_size=10)
            return cache_dict[(a, b, iter_count)]
        # Get all the pairs and compute the additional results
        result = _compute_value(a + b, pair_insertions, iter_size=10)
        total_values = dict()
        prev = None
        for ch in result:
            if prev is not None:
                pair_values = _compute_pair(prev, ch, iter_count=iter_count+1)
                # Extend
                for pair_ch in pair_values:
                    if pair_ch not in total_values:
                        total_values[pair_ch] = 0
                    total_values[pair_ch] += pair_values[pair_ch]
                total_values[ch] -= 1
            prev = ch
        total_values[result[-1]] += 1
        cache_dict[(a, b, iter_count)] = total_values
        return cache_dict[(a, b, iter_count)]

    prev = None
    total_counters = dict()
    for ch in start:
        if prev is not None:
            result_values = _compute_pair(prev, ch)
            for key_ch in result_values:
                if key_ch not in total_counters:
                    total_counters[key_ch] = 0
                total_counters[key_ch] += result_values[key_ch]
            total_counters[ch] -= 1
        prev = ch
    total_counters[start[-1]] += 1
    counter = collections.Counter(total_counters)
    _, most_common_count = counter.most_common(1)[0]
    _, least_common_count = counter.most_common()[-1]
    return most_common_count - least_common_count


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(*data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(*data)
    print("Solution 2: %d" % solution2)
