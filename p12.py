from utils import get_data_lines, log, permutations, get_data_as_lines
import re
from itertools import combinations_with_replacement as cwr


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


def part_one(datalines) -> int:
    sum = 0
    for dataline in datalines:
        map, runlengths = parse_dataline(dataline)
        sum += num_combinations(map, runlengths)
    return sum


if __name__ == '__main__':
    log.setLevel('DEBUG')

    sample, full = get_data_lines('12')
    log.debug(sample)
    sample_two = get_data_as_lines('12', 's2')
    log.debug(f"{parse_dataline(sample_two[0])=}")
    log.debug(find_unknowns(sample_two[1]))

    validate_sample_data(sample)

    sample_valid = part_one(sample)
    log.debug(f'{part_one(sample)=} should be 21')
