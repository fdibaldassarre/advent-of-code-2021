#!/usr/bin/env python3


MAPPINGS = {
    'abcefg': "0",
    'cf': "1",
    'acdeg': "2",
    'acdfg': "3",
    'bcdf': "4",
    'abdfg': "5",
    'abdefg': "6",
    'acf': "7",
    'abcdefg': "8",
    'abcdfg': "9"
}


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            patterns_raw, output_raw = line.strip().split(" | ")
            #patterns = patterns_raw.split(" ")
            patterns = list(map(lambda el: set(el), patterns_raw.split(" ")))
            output = output_raw.split(" ")
            data.append((patterns, output))
    return data


def find_mapping(patterns_set):
    patterns = [None] * 10
    # Find known patterns
    for candidate in patterns_set:
        if len(candidate) == 2:
            patterns[1] = candidate
        elif len(candidate) == 4:
            patterns[4] = candidate
        elif len(candidate) == 3:
            patterns[7] = candidate
        elif len(candidate) == 7:
            patterns[8] = candidate
    # Infer patterns
    # 3 if the only one with size 5 has intersection of size 2 with '1'
    # 2 is the only one with size 5 has intersection of size 2 with '4'
    # 5 is the only one with size 5 has intersection of size 3 with '4'
    for candidate in patterns_set:
        if len(candidate) == 5:
            if len(candidate.intersection(patterns[1])) == 2:
                patterns[3] = candidate
            else:
                int_size_with_4 = len(candidate.intersection(patterns[4]))
                if int_size_with_4 == 2:
                    patterns[2] = candidate
                elif int_size_with_4 == 3:
                    patterns[5] = candidate
    mapping = dict()
    # Map a, from 1 vs 7
    mapping['a'] = patterns[7].difference(patterns[1]).pop()
    # Map c, from 1 vs 2
    mapping['c'] = patterns[1].intersection(patterns[2]).pop()
    # Map f, from 1 minus pattern c
    mapping_f_set = set(patterns[1])
    mapping_f_set.remove(mapping['c'])
    mapping['f'] = mapping_f_set.pop()
    # Map e, from 2 minus 3
    mapping_e_set = patterns[2].difference(patterns[3])
    mapping['e'] = mapping_e_set.pop()
    # Find 0 pattern
    # 0 is the pattern with size 6 that has both c and e
    for candidate in patterns_set:
        if len(candidate) == 6 and mapping['c'] in candidate and mapping['e'] in candidate:
            patterns[0] = candidate
    # Map g, from 0 intersection 2, minus discovered a, c, e
    mapping_g_set = patterns[0].intersection(patterns[2])
    mapping_g_set.remove(mapping['a'])
    mapping_g_set.remove(mapping['c'])
    mapping_g_set.remove(mapping['e'])
    mapping['g'] = mapping_g_set.pop()
    # Map b from 0, minus discovered
    mapping_b_set = set(patterns[0])
    mapping_b_set.remove(mapping['a'])
    mapping_b_set.remove(mapping['c'])
    mapping_b_set.remove(mapping['e'])
    mapping_b_set.remove(mapping['f'])
    mapping_b_set.remove(mapping['g'])
    mapping['b'] = mapping_b_set.pop()
    # Map d, the last one
    mapping_d_set = set(patterns[2])
    mapping_d_set.remove(mapping['a'])
    mapping_d_set.remove(mapping['c'])
    mapping_d_set.remove(mapping['e'])
    mapping_d_set.remove(mapping['g'])
    mapping['d'] = mapping_d_set.pop()
    # Inverse the mapping
    inverse_mapping = dict()
    for el, value in mapping.items():
        inverse_mapping[value] = el
    return inverse_mapping


def decode_digit(output_digit, mapping):
    decoded_raw = list(map(lambda el: mapping[el], output_digit))
    decoded_raw.sort()
    decoded = "".join(decoded_raw)
    return MAPPINGS[decoded]


def decode(output, mappings):
    value = "".join(map(lambda digit: decode_digit(digit, mappings), output))
    return int(value)


def solve1(data):
    total = 0
    for _, output in data:
        for el in output:
            if len(el) == 2 or len(el) == 4 or len(el) == 7 or len(el) == 3:
                total += 1
    return total


def solve2(data):
    total = 0
    for patters, output in data:
        mappings = find_mapping(patters)
        value = decode(output, mappings)
        total += value
    return total


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
