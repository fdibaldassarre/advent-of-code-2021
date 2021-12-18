#!/usr/bin/env python3


SIDE_LEFT = 0
SIDE_RIGHT = 1


def parseOctoNumber(number, level=0):
    result = OctoNumber()
    result.level = level
    if type(number) == int:
        result.value = number
    else:
        result.setLeft(parseOctoNumber(number[0], level=level+1))
        result.setRight(parseOctoNumber(number[1], level=level+1))
    return result


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        for line in hand:
            data.append(parseOctoNumber(eval(line.strip())))
    return data


class OctoNumber:

    def __init__(self):
        self.level = 0
        self.parent = None
        self.side = None
        self.value = None
        self.left = None
        self.right = None

    def isPair(self):
        return self.value is None

    def setLeft(self, number):
        self.left = number
        number.parent = self
        number.side = SIDE_LEFT
        number.level = self.level + 1

    def setRight(self, number):
        self.right = number
        number.parent = self
        number.side = SIDE_RIGHT
        number.level = self.level + 1

    def nullify(self):
        zero_oct = OctoNumber()
        zero_oct.value = 0
        if self.side == SIDE_LEFT:
            self.parent.setLeft(zero_oct)
        else:
            self.parent.setRight(zero_oct)

    def clone(self):
        octoNumber = OctoNumber()
        octoNumber.level = self.level
        if self.isPair():
            octoNumber.setLeft(self.left.clone())
            octoNumber.setRight(self.right.clone())
        else:
            octoNumber.value = self.value
        return octoNumber


class OctoReducer:
    def __init__(self, number):
        self._number = number
        self.reduced = False
        self._add_next = None
        self.previous = None

    def reduce(self):
        self._reduceExplode(self._number)
        if self.reduced:
            return
        self._reduceSplit(self._number)

    def _reduceExplode(self, number):
        if self.reduced:
            if self._add_next is not None:
                if number.isPair():
                    self._reduceExplode(number.left)
                    self._reduceExplode(number.right)
                else:
                    number.value += self._add_next
                    self._add_next = None
            return
        if number.isPair():
            if number.level == 4:
                # Explode
                self._add_next = number.right.value
                if self.previous is not None:
                    self.previous.value += number.left.value
                self.reduced = True
                number.nullify()
            else:
                self._reduceExplode(number.left)
                self._reduceExplode(number.right)
        else:
            self.previous = number

    def _reduceSplit(self, number):
        if self.reduced:
            return
        if number.isPair():
            self._reduceSplit(number.left)
            self._reduceSplit(number.right)
        elif number.value >= 10:
            # Split
            rem = number.value % 2
            left_size = OctoNumber()
            left_size.value = number.value // 2
            number.setLeft(left_size)
            right_size = OctoNumber()
            right_size.value = number.value // 2 + rem
            number.setRight(right_size)
            number.value = None
            self.reduced = True


def _reduce(number):
    while True:
        parser = OctoReducer(number)
        parser.reduce()
        if not parser.reduced:
            break


def _get_magnitude(number):
    if number.isPair():
        return 3 * _get_magnitude(number.left) + 2 * _get_magnitude(number.right)
    else:
        return number.value


def _update_levels(number, level=0):
    number.level = level
    if number.isPair():
        _update_levels(number.left, level=level+1)
        _update_levels(number.right, level=level+1)


def _sum_octonumbers(a, b):
    octo_sum = OctoNumber()
    octo_sum.setLeft(a.clone())
    octo_sum.setRight(b.clone())
    _update_levels(octo_sum)
    _reduce(octo_sum)
    return octo_sum


def solve1(numbers):
    current = numbers[0]
    for i in range(1, len(numbers)):
        octo_sum = _sum_octonumbers(current, numbers[i])
        current = octo_sum
    return _get_magnitude(current)


def solve2(numbers):
    max_mag = -1
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            a, b = numbers[i], numbers[j]
            sum_ab = _sum_octonumbers(a, b)
            sum_ba = _sum_octonumbers(b, a)
            max_mag = max(max_mag, _get_magnitude(sum_ab), _get_magnitude(sum_ba))
    return max_mag


if __name__ == "__main__":
    data = parse("input")
    solution1 = solve1(data)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(data)
    print("Solution 2: %d" % solution2)
