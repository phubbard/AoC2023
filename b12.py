from utils import get_data_lines, log
from functools import lru_cache

import time

OPERATIONAL_CHAR = '.'
DAMAGED_CHAR     = '#'
UNKNOWN_CHAR     = '?'



presample_data = \
"""#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1""".split('\n')

raw_12s2_data = \
"""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split('\n')


def count_permutations(locked_variables, sum_remnant, remaining_variable_count, debug):
    if remaining_variable_count == 1:
        if debug:
            permutation = locked_variables + (sum_remnant,)
            log.info(f"  {permutation}")
        return 1
    total = 0
    for i in range(sum_remnant - 1):
        value = i + 1
        total += count_permutations(locked_variables + (value,), sum_remnant - value, remaining_variable_count - 1, debug)
    return total


def count_hashtags(map: list) -> int:
    count = 0
    while count < len(map) and map[count] == '#':
        count += 1
    return count

TABS = ' '

@lru_cache(maxsize=None)
def p2_search(indent, condition_record, contiguous_group) -> int:
    if indent: indent += TABS
    # Implementing the algo by dmaltor1 in https://www.reddit.com/r/adventofcode/comments/18ghux0/2023_day_12_no_idea_how_to_start_with_this_puzzle/
    # log.info(f'{len(indent)}: {indent}: {''.join(condition_record)} {contiguous_group=}')
    if len(condition_record) == 0:
        if len(contiguous_group) > 0:
            return 0
        else:
            # log.info(f'{len(indent)}: {indent}: FOUND!')
            return 1

    if condition_record[0] == '.':
        return p2_search(indent, tuple(condition_record[1:]), contiguous_group)

    if condition_record[0] == '?':
        left_map = list(condition_record)
        left_map[0] = '.'
        right_map = list(condition_record)
        right_map[0] = '#'
        return p2_search(indent, tuple(left_map), contiguous_group) + \
               p2_search(indent, tuple(right_map), contiguous_group)

    if condition_record[0] == '#':
        # find the length of the run of # characters
        if len(contiguous_group) == 0:
            return 0
        must_consume_count = contiguous_group[0]
        if must_consume_count > len(condition_record):
            return 0
        
        for i in range(must_consume_count):
            if condition_record[i] == '.':
                return 0
            
        new_condition_record = list(condition_record)[must_consume_count:]
        new_contiguous_group = tuple(list(contiguous_group)[1:])

        if len(new_condition_record) > 0:
            if new_condition_record[0] == '#':
                return 0
            new_condition_record[0] = '.'
            # log.info(f'{len(indent)}: {indent}: about to consider {new_condition_record=}')
        return p2_search(indent, tuple(new_condition_record), new_contiguous_group)


if __name__ == '__main__':

    def __permutation_study():
        N, c = 10, 5
        total = count_permutations((), N, c, True)
        log.info(f"Permutation study for {N=} {c=} is {total}")
        prev_time = time.time()
        c = 6
        # ?#?????????????????? 2,1,1,2,7,1
        for N in range(10, 40):
            total = count_permutations((), N, c, False)
            curr_time = time.time()
            log.info(f"{curr_time - prev_time}: Permutation study for {N=} {c=} is {total}")
            prev_time = curr_time
    __permutation_study()

    sample_data, full_data = get_data_lines('12')

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,      -1),
                ("raw_s2", raw_12s2_data,     21,  525152),
                # ("full",   full_data,       8180,      -1),
            ]:

        if expected_p1_answer > -1:
            arrangement_count = 0
            for row in dataset:

                cr_string, cg_string = row.split(' ')
                condition_record = tuple(c for c in cr_string)
                contiguous_group = tuple(int(c) for c in cg_string.split(','))
                log.info(f"Considering -> {row} {condition_record=} {contiguous_group=}")
                arrangement_count += p2_search('', condition_record, contiguous_group)

            found_p1_answer = arrangement_count
            log.info(f"Steps: {found_p1_answer=} with {expected_p1_answer=}")
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        found_p2_answer = 0
        log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
        if expected_p2_answer > -1:
            prev_time = time.time()
            arrangement_count = 0
            for row in dataset:
                log.info(f"For row -> {row=}")
                cr_string, cg_string = row.split(' ')

                log.info(f"  -> {cr_string=} and {cg_string=}")

                cr_string = '?'.join([cr_string] * 5)
                cg_string = ','.join([cg_string] * 5)

                log.info(f"  -> {cr_string=} and {cg_string=}")

                log.info(f"   transforming -> {cr_string=}")
                condition_record = tuple(c for c in cr_string)
                log.info(f"  ... to  {condition_record=}")

                contiguous_group = tuple(int(c) for c in cg_string.split(','))
                curr_time = time.time()

                #log.info(f"Considering -> {row} as {''.join(condition_record)}")
                #log.info(f"               {contiguous_group=}")
                permutations = p2_search('', condition_record, contiguous_group)
                log.info(f"{curr_time - prev_time}:  found {permutations} permutations for {row}")
                arrangement_count += permutations
                prev_time = curr_time
            found_p2_answer = arrangement_count

            log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")


