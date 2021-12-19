#!/usr/bin/env python3


def parse(input_file):
    data = list()
    with open(input_file, "r") as hand:
        beacons = list()
        for line in hand:
            line = line.strip()
            if line == "":
                data.append(beacons)
                beacons = list()
                continue
            if line.startswith("---"):
                continue
            beacon = tuple(map(int, line.split(",")))
            beacons.append(beacon)
    if len(beacons) > 0:
        data.append(beacons)
    return data


def get_distance(a, b):
    d = [0] * len(a)
    for i in range(len(d)):
        d[i] = a[i] - b[i]
    return tuple(d)


def translate(a, d):
    r = [0] * len(a)
    for i in range(len(a)):
        r[i] = a[i] + d[i]
    return tuple(r)



class ScannerPoints:

    def __init__(self, beacons):
        self._beacons = beacons
        self._differences = None
        self._differences_map = None
        self._difference_abs_vectors = None
        self.views = dict()

    def getBeacons(self):
        return set(self._beacons)

    def getBeacon(self, idx):
        return self._beacons[idx]

    def _computeDiff(self):
        diff = dict()
        for i in range(len(self._beacons)):
            for j in range(len(self._beacons)):
                if i != j:
                    diff[(i, j)] = get_distance(self._beacons[i], self._beacons[j])
        self._differences = diff
        self._differences_map = dict()
        self._difference_abs_vectors = dict()
        for point, dist in self._differences.items():
            if dist not in self._differences_map:
                self._differences_map[dist] = list()
            self._differences_map[dist].append(point)
            vect = list(map(abs, dist))
            vect.sort()
            vect = tuple(vect)
            if vect not in self._difference_abs_vectors:
                self._difference_abs_vectors[vect] = set()
            self._difference_abs_vectors[vect].add(dist)

    def getDifferenceAbsVectors(self):
        if self._difference_abs_vectors is None:
            self._computeDiff()
        return self._difference_abs_vectors

    def getDifferences(self):
        if self._differences is None:
            self._computeDiff()
        return self._differences

    def getDifferencesMap(self):
        if self._differences_map is None:
            self._computeDiff()
        return self._differences_map

    def translateBeacons(self, delta):
        new_beacons = set()
        for beacon in self._beacons:
            new_beacons.add(translate(beacon, delta))
        return new_beacons

    def applyTransformation(self, transformation):
        idx, transform = transformation
        if idx not in self.views:
            new_beacons = list(map(transform, self._beacons))
            self.views[idx] = ScannerPoints(new_beacons)
        return self.views[idx]


def transform_coordinates(scanner, reference):
    for points, delta in reference.getDifferences().items():
        # Try to map points into scanner2
        if delta not in scanner.getDifferencesMap():
            continue
        for other_points in scanner.getDifferencesMap().get(delta):
            # Candidate
            translation = get_distance(reference.getBeacon(points[0]), scanner.getBeacon(other_points[0]))
            # Attempt to translate scanner2 beacons and verify at least 12 beacons match
            new_beacons = scanner.translateBeacons(translation)
            intersection = len(reference.getBeacons().intersection(new_beacons))
            if intersection >= 12:
                # Valid translation
                return translation, new_beacons
    return None



def get_all_rotations():
    yield lambda x, y, z: (x, y, z)
    yield lambda x, y, z: (x, -z, y)
    yield lambda x, y, z: (x, -y, -z)
    yield lambda x, y, z: (x, z, -y)
    yield lambda x, y, z: (-z, y, x)
    yield lambda x, y, z: (-x, y, -z)
    yield lambda x, y, z: (-z, y, -x)
    yield lambda x, y, z: (-y, x, z)
    yield lambda x, y, z: (-x, -y, z)
    yield lambda x, y, z: (-y, -x, z)

    yield lambda x, y, z: (-x, y, z)
    yield lambda x, y, z: (-x, -z, y)
    yield lambda x, y, z: (-x, -y, -z)
    yield lambda x, y, z: (-x, z, -y)

    yield lambda x, y, z: (-z, -y, x)
    yield lambda x, y, z: (-x, -y, -z)
    yield lambda x, y, z: (-z, -y, -x)

    yield lambda x, y, z: (-y, x, -z)
    yield lambda x, y, z: (-x, -y, -z)
    yield lambda x, y, z: (-y, -x, -z)


def get_all_transfomrations():
    idx = 0
    for rotation1 in get_all_rotations():
        for rotation2 in get_all_rotations():
            yield idx, lambda v: rotation2(*rotation1(*v))
            idx += 1


def _possible_mappings(scanner, reference):
    distances = scanner.getDifferenceAbsVectors().keys()
    ref_distance = reference.getDifferenceAbsVectors().keys()
    intersection = set(distances).intersection(ref_distance)
    if len(intersection) == 0:
        return None
    return intersection


def is_possible_transform(transformation, possible_mappings, scanner, reference):
    for candidate in possible_mappings:
        sources = scanner.getDifferenceAbsVectors()[candidate]
        targets = set(reference.getDifferenceAbsVectors()[candidate])
        for source in sources:
            if transformation(source) in targets:
                return True
    return False


def normalize_coordinates(original_scanner, reference):
    possible_mappings = _possible_mappings(original_scanner, reference)
    if possible_mappings is None:
        return None
    for transformation in get_all_transfomrations():
        if not is_possible_transform(transformation[1], possible_mappings, original_scanner, reference):
            continue
        scanner = original_scanner.applyTransformation(transformation)
        result = transform_coordinates(scanner, reference)
        if result is not None:
            return result
    return None


def solve1(scanners):
    unknown = list()
    for i in range(1, len(scanners)):
        scanner = ScannerPoints(scanners[i])
        unknown.append(scanner)

    known = set()
    known.add(ScannerPoints(scanners[0]))

    all_beacons = set(scanners[0])
    positions = list()
    positions.append((0, 0, 0))
    while len(unknown) > 0:
        new_unknowns = set()
        ref = known.pop()
        for scanner in unknown:
            result = normalize_coordinates(scanner, ref)
            if result is None:
                # No intersections with this scanner...
                new_unknowns.add(scanner)
            else:
                transformation, normalized = result
                positions.append(transformation)
                known.add(ScannerPoints(list(normalized)))
                all_beacons = all_beacons.union(normalized)
        unknown = new_unknowns

    max_dist = 0
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            max_dist = max(max_dist, get_l0_distance(positions[i], positions[j]))

    return len(all_beacons), max_dist


def get_l0_distance(a, b):
    r = 0
    for i in range(len(a)):
        r += abs(a[i] - b[i])
    return r


if __name__ == "__main__":
    data = parse("input")
    solution1, solution2 = solve1(data)
    print("Solution 1: %d" % solution1)
    print("Solution 2: %d" % solution2)
