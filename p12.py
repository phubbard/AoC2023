from utils import get_data_lines, log, permutations, get_data_as_lines
import re
from itertools import product


def find_unknowns(dataline) -> list:
    # Find the unknowns in a dataline
    return re.findall(r'(\?+)', dataline)


def find_damaged(dataline) -> list:
    # Find the damaged parts of a dataline
    return re.findall(r'(\#+)', dataline)


def validate(dataline, runlength) -> bool:
    # Validate datalines against runlengths
    damaged = find_damaged(dataline)
    if len(damaged) != len(runlength):
        return False
    for dmged, runlength in zip(damaged, runlength):
        if len(dmged) != runlength:
            return False
    return True


def parse_dataline(dataline) -> tuple:
    tokens = dataline.split(' ')
    map = tokens[0]
    runlengths = [int(x) for x in tokens[1].split(',')]

    return map, runlengths


def validate_sample_data(datalines):
    # Validate the sample data
    for dataline in datalines:
        map, runlengths = parse_dataline(dataline)
        log.debug(f'Validating {map} against {runlengths}')
        log.debug(f'Unknowns: {find_unknowns(map)}')
        log.debug(f'Damaged: {find_damaged(map)}')
        log.debug(f'Valid: {validate(map, runlengths)}')


def num_combinations(dataline, runlengths) -> int:
    rc = 0
    unknowns = find_unknowns(dataline)
    total_unk_length = sum([len(x) for x in unknowns])
    possiblities = product('.#', repeat=total_unk_length)
    for possibility in possiblities:
        p_str = ''.join(possibility)
        # via https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
        unk_indices = [m.start() for m in re.finditer(r'\?', dataline)]
        # Build a new dataline with the unknowns replaced by the possibility
        new_dataline = list(dataline)
        for p_idx, u_idx in enumerate(unk_indices):
            new_dataline[u_idx] = p_str[p_idx]
        if validate(''.join(new_dataline), runlengths):
            rc += 1
    return rc


def part_one(datalines) -> int:
    sum = 0
    for dataline in datalines:
        map, runlengths = parse_dataline(dataline)
        sum += num_combinations(map, runlengths)
    return sum


if __name__ == '__main__':
    log.setLevel('INFO')

    sample, full = get_data_lines('12')
    log.debug(sample)
    sample_two = get_data_as_lines('12', 's2')
    log.debug(f"{parse_dataline(sample_two[0])=}")
    log.debug(find_unknowns(sample_two[1]))

    validate_sample_data(sample)

    assert(num_combinations(sample_two[0], [1, 1, 3]) == 1)
    map, rl = parse_dataline(sample_two[1])
    assert(num_combinations(map, rl) == 4)

    sample_valid = part_one(sample)
    log.info(f'{part_one(sample_two)=} should be 21')

    log.info(f'{part_one(full)=} should be 8180')
    p1_answer = 8180
