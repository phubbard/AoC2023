from utils import load_2d_arrays, log, manhattan_distance


def find_galaxies(data) -> list:
    # Find all the galaxies in the data
    galaxies = []
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == '#':
                galaxies.append([row, col])
    return galaxies


def find_empty(galaxies, max_count: int, dimension: int, increment: int = 1) -> list:
    # dim = 0 for rows, dim = 1 for cols
    empty_set = []
    for idx in range(max_count):
        if not any([x[dimension] == idx for x in galaxies]):
            # After we add a col, the rest of the list needs to be incremented to match.
            empty_set.append(idx + len(empty_set) * (increment - 1))
    return empty_set


def expand_galaxies(galaxies, matrix, increment=2) -> list:
    # As per rules, for each empty row and col, add another adjacent row or col.
    # Since we're storing (row,col) this is just addition.
    empty_c = find_empty(galaxies, len(matrix[0]), 1, increment=increment)
    empty_r = find_empty(galaxies, len(matrix), 0, increment=increment)
    for col in empty_c:
        for gal in galaxies:
            if gal[1] > col:
                gal[1] += increment - 1
    for row in empty_r:
        for gal in galaxies:
            if gal[0] > row:
                gal[0] += increment - 1

    return galaxies


def pairwise_distances(galaxies):
    distances = []
    for idx in range(len(galaxies)):
        for idx2 in range(idx + 1, len(galaxies)):
            distances.append(manhattan_distance(galaxies[idx], galaxies[idx2]))
    return distances


def all_sum(galaxies) -> int:
    distances = pairwise_distances(galaxies)
    return sum(distances)


def print_galaxies(galaxies):
    for idx, gal in enumerate(galaxies):
        log.info(f"{idx + 1} : {gal[0]},{gal[1]}")


if __name__ == '__main__':
    sample, full = load_2d_arrays(11)
    galaxies = find_galaxies(sample)
    expanded = expand_galaxies(galaxies, sample)

    distance = manhattan_distance(expanded[4], expanded[8])
    assert(distance == 9)
    distance = manhattan_distance(expanded[0], expanded[6])
    assert(distance == 15)
    distance = manhattan_distance(expanded[2], expanded[5])
    assert(distance == 17)
    i = manhattan_distance(expanded[7], expanded[8])
    assert(i == 5)

    p1_answer = 9545480
    p2_answer = 406725732046
    log.info(f"sample: {all_sum(expanded)} 374")

    galaxies = find_galaxies(full)
    expanded = expand_galaxies(galaxies, full)
    log.info(f"full: {all_sum(expanded)} {p1_answer=}")

    # Part 2 test - 10x
    galaxies = find_galaxies(sample)
    expanded = expand_galaxies(galaxies, sample, increment=10)
    log.info(f"sample: {all_sum(expanded)} 1030")
    # Part 2
    galaxies = find_galaxies(full)
    expanded = expand_galaxies(galaxies, full, increment=1000000)
    log.info(f"full: {all_sum(expanded)} {p2_answer=}")

