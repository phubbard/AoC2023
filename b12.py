from utils import get_data_lines, log


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
        springs, groups = row.split(' ')


    def __repr__(self):
        return f"C[{self.CONDITION}]"

presample_data = \
"""#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1""".split('\n')


if __name__ == '__main__':

    def __presample_check():
        for row in presample_data:
            condition, expected_score = row.split(' ')
            arrangement = Arrangement(condition)
            log.info(f"expecting {expected_score} to be {arrangement.ARRANGEMENT_SCORE}")
            assert arrangement.ARRANGEMENT_SCORE == expected_score
    __presample_check()

    sample_data, full_data = get_data_lines('12')

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,      -1),
                ("full",   full_data,         -1,      -1),
            ]:
        log.info(f"Considering -> {tag}")

        # log.info(f"{dataset=}")

        found_p1_answer = 0
        log.info(f"Steps: {found_p1_answer=} with {expected_p1_answer=}")
        if expected_p1_answer > -1:
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        found_p2_answer = 0
        log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
        if expected_p2_answer > -1:
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")


