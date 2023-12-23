from itertools import permutations
from utils import load_2d_arrays, log, manhattan_distance


def find_galaxies(data) -> list:
    # Find all the galaxies in the data
    galaxies = []
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == '#':
                galaxies.append([row, col])
    return galaxies


def find_empty(galaxies, max_count: int, dimension: int) -> list:
    # dim = 0 for rows, dim = 1 for cols
    empty_set = []
    for idx in range(max_count):
        if not any([x[dimension] == idx for x in galaxies]):
            empty_set.append(idx)
    return empty_set


def expand_galaxies(galaxies, matrix) -> list:
    # As per rules, for each empty row and col, add another adjacent row or col.
    # Since we're storing (row,col) this is just addition.
    empty_c = find_empty(galaxies, len(matrix[0]), 1)
    empty_r = find_empty(galaxies, len(matrix), 0)
    for col in empty_c:
        for gal in galaxies:
            if gal[1] > col:
                gal[1] += 1
    for row in empty_r:
        for gal in galaxies:
            if gal[0] > row:
                gal[0] += 1

    return galaxies


def pairwise_distances(galaxies):
    # Data struct is (row,col,row2,col2,distance)
    distances = []
    for idx, gal in enumerate(galaxies):
        for idx2, gal2 in enumerate(galaxies):
            if idx == idx2:
                continue
            distances.append([gal[0], gal[1], gal2[0], gal2[1], manhattan_distance(gal, gal2)])
    # Now we need to de-duplicate. (a,b) is the same as (b,a)
    # We can do this by sorting the first two elements of each row.

    distances = [sorted(x) for x in distances]
    distances = sorted(distances)
    distances = [x for x in distances if x[0] != x[2] or x[1] != x[3]]

    return distances


def all_sum(galaxies) -> int:
    distances = pairwise_distances(galaxies)
    return sum([x[4] for x in distances])


if __name__ == '__main__':
    sample, full = load_2d_arrays(11)
    galaxies = find_galaxies(sample)
    expanded = expand_galaxies(galaxies, sample)
    empty_c = find_empty(expanded, len(sample[0]), 1)
    empty_r = find_empty(expanded, len(sample), 0)
    log.info(f"expanded {empty_c=} {empty_r=}")

    distance = manhattan_distance(expanded[4], expanded[8])
    assert(distance == 9)
    distance = manhattan_distance(expanded[0], expanded[6])
    # assert(distance == 15)
    distance = manhattan_distance(expanded[2], expanded[5])
    assert(distance == 17)
    i = manhattan_distance(expanded[7], expanded[8])
    assert(i == 5)

    log.info(f"sample: {all_sum(galaxies)}")