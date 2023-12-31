from utils import get_data_lines, log, permutations, get_data_as_lines
import re
from functools import lru_cache
from itertools import product
from multiprocessing import Pool, cpu_count


def find_unknowns(dataline) -> list:
    # Find the unknowns in a dataline
    return re.findall(r'(\?+)', dataline)


def find_damaged(dataline) -> list:
    # Find the damaged parts of a dataline
    return re.findall(r'(#+)', dataline)


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
    for dataline in datalines:
        map, runlengths = parse_dataline(dataline)
        log.debug(f'Validating {map} against {runlengths}')
        # log.debug(f'Unknowns: {find_unknowns(map)}')
        # log.debug(f'Damaged: {find_damaged(map)}')
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


def p1_worker(dataline) -> int:
    map, runlengths = parse_dataline(dataline)
    return num_combinations(map, runlengths)


def p1_mp(datalines) -> int:
    # Multiprocessing version of part one
    pool = Pool()
    log.info(f'{cpu_count()=}')
    results = pool.map(p1_worker, datalines)
    return sum(results)


def part_one(datalines) -> int:
    total_sum = 0
    for dataline in datalines:
        map, runlengths = parse_dataline(dataline)
        total_sum += num_combinations(map, runlengths)
    return total_sum


def ptwo_expand(rawline):
    # Easier to re-parse the line than to try to expand it
    tokens = rawline.split(' ')
    left = (tokens[0] + '?') * 5
    left = left[:-1]
    right = (tokens[1] + ',') * 5
    right = right[:-1]
    return f'{left} {right}'


def p2_worker(dataline):
    log.info(f'Processing {dataline}')
    expanded = ptwo_expand(dataline)
    map, runlengths = parse_dataline(expanded)
    log.info(f'Processing combinations for {map} against {runlengths}')
    return num_combinations(map, runlengths)


def part_two(datalines) -> int:
    pool = Pool()
    log.info(f'part two {cpu_count()=}')
    results = pool.map(p2_worker, datalines)
    log.info(f'{sum(results)=}')
    return sum(results)


# @lru_cache(maxsize=None)
def p2_search(map: list, runlengths: list) -> int:
    # Implementing the algo by dmaltor1 in https://www.reddit.com/r/adventofcode/comments/18ghux0/2023_day_12_no_idea_how_to_start_with_this_puzzle/
    log.debug(f'{map=} {runlengths=}')
    if len(map) == 0:
        if len(runlengths) > 0:
            return 0
        else:
            log.debug('Found a match')
            return 1

    if map[0] == '.':
        return p2_search(map[1:], runlengths)

    if map[0] == '?':
        left_map = map.copy()
        left_map[0] = '.'
        right_map = map.copy()
        right_map[0] = '#'
        return p2_search(left_map, runlengths) + p2_search(right_map, runlengths)

    if map[0] == '#':
        if len(runlengths) == 0:
            return 0
        # find the length of the run of # characters
        count = 0
        while count < len(map) and map[count] == '#':
            count += 1

        if count == runlengths[0]:
            return p2_search(map[count:], runlengths[1:])
        else:
            # May be wrong logic here
            return 0


if __name__ == '__main__':
    log.setLevel('DEBUG')

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
    log.info(f'{p1_mp(sample_two)=} should be 21')

    # log.info(f'{part_one(full)=} should be 8180')
    # log.info(f'{p1_mp(full)=} should be 8180')

    p1_answer = 8180
    inp= '???.### 1,1,3'  # one answer
    ref = '???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3'
    ans = ptwo_expand(inp)
    assert(ptwo_expand(inp) == ref)
    test_dataline = '?###???????? 3,2,1'
    test_exp = ptwo_expand(test_dataline)
    tmap, rll = parse_dataline(inp)
    test_ans = 506250
    t_list = list(tmap)
    log.info(p2_search(t_list, rll))
    # log.info(f'{=} should be {test_ans}')
    # log.info(f'{part_two(sample_two)=} should be 525152')
