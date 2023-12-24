from utils import get_data_lines, log

import time

OPERATIONAL_CHAR = '.'
DAMAGED_CHAR     = '#'
UNKNOWN_CHAR     = '?'

class Arrangement:
    def __init__(self, string):
        score_prep = string.split(OPERATIONAL_CHAR)
        score_lengths = [len(score) for score in score_prep if len(score) > 0]

        self.ARRANGEMENT_STRING  = string
        self.ARRANGEMENT_SCORE   = ','.join([str(score) for score in score_lengths])

    def __repr__(self):
        return f"S[{self.ARRANGEMENT_STRING} {self.ARRANGEMENT_SCORE}]"


class Condition:
    def __init__(self, row):
        springs, score = row.split(' ')
        # log.info(f"Considering {springs=} with {score=}")

        unknown_indices = []
        for idx, char in enumerate(springs):
            if char == UNKNOWN_CHAR:
                unknown_indices.append(idx)
        
        # log.info(f"  {unknown_indices=}")
        self.CONDITION_UNKNOWN_INDICES = tuple(unknown_indices)
        self.CONDITION_SCORE           = score
        self.CONDITION_SPRINGS         = springs


    def generate_valid_arrangements(self):
        unknown_indices = self.CONDITION_UNKNOWN_INDICES
        # Generate all possible arrangements
        valid_arrangements = []
        for seed in range(2 ** len(unknown_indices)):
            arrangement_root = [c for c in self.CONDITION_SPRINGS]
            for idx, bit in enumerate(unknown_indices):
                arrangement_root[bit] = OPERATIONAL_CHAR if (seed & (1 << idx)) else DAMAGED_CHAR

            arrangement = Arrangement(''.join(arrangement_root))
            if arrangement.ARRANGEMENT_SCORE == self.CONDITION_SCORE:
                valid_arrangements.append(arrangement)
        return tuple(valid_arrangements)


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

def p2_search(indent, condition_record: list, contiguous_group: list) -> int:
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
        return p2_search(indent, condition_record[1:], contiguous_group)

    if condition_record[0] == '?':
        left_map = condition_record.copy()
        left_map[0] = '.'
        right_map = condition_record.copy()
        right_map[0] = '#'
        return p2_search(indent, left_map, contiguous_group) + \
               p2_search(indent, right_map, contiguous_group)

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
            
        new_condition_record = condition_record[must_consume_count:]
        new_contiguous_group = contiguous_group[1:]

        if len(new_condition_record) > 0:
            if new_condition_record[0] == '#':
                return 0
            new_condition_record[0] = '.'
            # log.info(f'{len(indent)}: {indent}: about to consider {new_condition_record=}')
        return p2_search(indent, new_condition_record, new_contiguous_group)


if __name__ == '__main__':

    def __presample_check():
        for row in presample_data:
            condition, expected_score = row.split(' ')
            arrangement = Arrangement(condition)
            log.info(f"expecting {expected_score} to be {arrangement.ARRANGEMENT_SCORE}")
            assert arrangement.ARRANGEMENT_SCORE == expected_score
    __presample_check()

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

    def __paul_impl_study():
        for row in ['?###???????? 3,2,1']:
            cr_string, cg_string = row.split(' ')
            condition_record = [c for c in cr_string]
            contiguous_group = [int(c) for c in cg_string.split(',')]
            log.info(f"Considering -> {row} {condition_record=} {contiguous_group=}")
            result = p2_search('', condition_record, contiguous_group)
            log.info(f"  {result=}")
    __paul_impl_study()

    sample_data, full_data = get_data_lines('12')

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,      -1),
                ("raw_s2", raw_12s2_data,     21,      1),
                ("full",   full_data,       8180,      -1),
            ]:

        if expected_p1_answer > -1:
            arrangement_count = 0
            for row in dataset:

                cr_string, cg_string = row.split(' ')
                condition_record = [c for c in cr_string]
                contiguous_group = [int(c) for c in cg_string.split(',')]
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
                cr_string, cg_string = row.split(' ')

                cr_string = '?'.join(cr_string * 5)
                cg_string = ','.join([cg_string] * 5)

                condition_record = [c for c in cr_string]
                contiguous_group = [int(c) for c in cg_string.split(',')]
                curr_time = time.time()

                log.info(f"Considering -> {row} {condition_record=} {contiguous_group=}")
                permutations = p2_search('', condition_record, contiguous_group)
                log.info(f"{curr_time - prev_time}:  found {permutations} permutations for {row}")
                arrangement_count += permutations
                prev_time = curr_time

            assert found_p2_answer == expected_p2_answer
            log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
        else:
            log.info(f"Skipping part two")


