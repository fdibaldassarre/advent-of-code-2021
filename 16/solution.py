#!/usr/bin/env python3


HEX_CONVERSION = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

TYPE_SUM = 0
TYPE_PROD = 1
TYPE_MIN = 2
TYPE_MAX = 3
TYPE_LITERAL_VALUE = 4
TYPE_GREATER_THAN = 5
TYPE_LESS_THAN = 6
TYPE_EQUAL_TO = 7

LENGTH_MODE_BITS = 0
LENGTH_MODE_COUNT = 1

def parse(input_file):
    with open(input_file, "r") as hand:
        data = hand.readline().strip()
    return data


def _hex_to_binary(hexadecimal_string):
    result = list()
    for ch in hexadecimal_string:
        for bit in HEX_CONVERSION[ch]:
            result.append(int(bit))
    return result


def _binary_to_int(bin_val):
    result = 0
    for bit in bin_val:
        result = 2 * result + bit
    return result


PACKET_LITERAL = 0
PACKET_CONTAINER = 1

class Packet:
    def __init__(self, version, type_id, type):
        self.version = version
        self.type_id = type_id
        self.type = type

class LiteralPacket(Packet):
    def __init__(self, version, type_id, value):
        super().__init__(version, type_id, PACKET_LITERAL)
        self.value = value


class ContainerType(Packet):
    def __init__(self, version, type_id, packets):
        super().__init__(version, type_id, PACKET_CONTAINER)
        self.packets = packets

class BinParser:

    def __init__(self, bin_string):
        self.bin_string = bin_string
        self.cursor = 0

    def _read_bits(self, n_bits):
        result = list()
        for _ in range(n_bits):
            result.append(self._read_bit())
        return result

    def _read_bit(self):
        res = self.bin_string[self.cursor]
        self.cursor += 1
        return res

    def parse(self):
        self._parsed = self._parse_packet()
        return self._parsed

    def parse_packets(self):
        packets = list()
        while self.cursor < len(self.bin_string):
            packet = self._parse_packet()
            packets.append(packet)
        return packets

    def _parse_packet(self):
        version = _binary_to_int(self._read_bits(3))
        type_id = _binary_to_int(self._read_bits(3))
        if type_id == TYPE_LITERAL_VALUE:
            # print("Lit",bin_string[start+6:end])
            literal_value = self._parse_literal_value()
            return LiteralPacket(version, type_id, literal_value)
        else:
            packets = self._parse_container()
            return ContainerType(version, type_id, packets)

    def _parse_literal_value(self):
        result = list()
        while True:
            header_bit = self._read_bit()
            result.extend(self._read_bits(4))
            if header_bit == 0:
                break
        return _binary_to_int(result)

    def _parse_container(self):
        type_id = self._read_bit()
        if type_id == LENGTH_MODE_BITS:
            bit_length = _binary_to_int(self._read_bits(15))
            packets_bin = self._read_bits(bit_length)
            parser = BinParser(packets_bin)
            packets = parser.parse_packets()
            return packets
        elif type_id == LENGTH_MODE_COUNT:
            n_packets = _binary_to_int(self._read_bits(11))
            packets = list()
            for _ in range(n_packets):
                packet = self._parse_packet()
                packets.append(packet)
            return packets
        else:
            raise RuntimeError("Invalid container type")


def eval_packet(packet):
    if packet.type_id == TYPE_LITERAL_VALUE:
        return packet.value
    else:
        sub_packets = packet.packets
        sub_values = list(map(eval_packet, sub_packets))
        if packet.type_id == TYPE_SUM:
            return sum(sub_values)
        elif packet.type_id == TYPE_PROD:
            res = 1
            for val in sub_values:
                res *= val
            return res
        elif packet.type_id == TYPE_MIN:
            return min(sub_values)
        elif packet.type_id == TYPE_MAX:
            return max(sub_values)
        elif packet.type_id == TYPE_GREATER_THAN:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif packet.type_id == TYPE_LESS_THAN:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif packet.type_id == TYPE_EQUAL_TO:
            return 1 if sub_values[0] == sub_values[1] else 0
        else:
            raise RuntimeError("Invalid operation")


def solve1(binary_string):
    parser = BinParser(binary_string)
    packet = parser.parse()

    def count_versions(node):
        if node.type == PACKET_LITERAL:
            return node.version
        else:
            total = node.version
            for sub_packet in node.packets:
                total += count_versions(sub_packet)
            return total
    return count_versions(packet)


def solve2(binary_string):
    parser = BinParser(binary_string)
    packet = parser.parse()
    return eval_packet(packet)


if __name__ == "__main__":
    data = parse("input")
    binary_string = _hex_to_binary(data)
    solution1 = solve1(binary_string)
    print("Solution 1: %d" % solution1)
    solution2 = solve2(binary_string)
    print("Solution 2: %d" % solution2)
