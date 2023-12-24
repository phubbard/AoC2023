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

    raise Exception("Done for now")

    sample_data, full_data = get_data_lines('12')

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,      -1),
                ("raw_s2", raw_12s2_data,     21,      -1),
                ("full",   full_data,       8180,      -1),
            ]:
        log.info(f"Considering -> {tag}")

        if expected_p1_answer > -1:
            arrangement_count = 0
            for row in dataset:
                condition = Condition(row)
                log.info(f"{len(condition.CONDITION_UNKNOWN_INDICES)} permutations for {condition.CONDITION_SPRINGS} {condition.CONDITION_SCORE}")
                valid_arrangements = condition.generate_valid_arrangements()
                arrangement_count += len(valid_arrangements)
            found_p1_answer = arrangement_count
            log.info(f"Steps: {found_p1_answer=} with {expected_p1_answer=}")
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        found_p2_answer = 0
        log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
        if expected_p2_answer > -1:
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")


