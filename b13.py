from utils import get_data_lines, log

sample_data = [
    "#.##..##.",
    "..#.##.#.",
    "##......#",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
    "",
    "#...##..#",
    "#....#..#",
    "..##..###",
    "#####.##.",
    "#####.##.",
    "..##..###",
    "#....#..#",
]


CHAR_ASH   = '.'
CHAR_ROCKS = '#'


class Analysis:
    def __init__(self, strings, multiplier):
        candidate_prefold_indices = []
        total_strings = len(strings)

        log.info(f"Pattern view for {multiplier}...")
        for string in strings: log.info(f"  {string}")

        for hypothesis_index in range(total_strings - 1):
            last_unfolded_index = hypothesis_index + 1
            good_match = True
            for match_index in range(total_strings):
                index1 = hypothesis_index - match_index
                index2 = hypothesis_index + match_index + 1
                if index1 < 0 or index2 >= total_strings: break
                if strings[index1] != strings[index2]:
                    good_match = False
                    break
            if good_match:
                candidate_prefold_indices.append(last_unfolded_index)
        log.info(f"  {candidate_prefold_indices=}")

        self.ANALYSIS_SCORE = multiplier * sum(candidate_prefold_indices)


class Pattern:
    def __init__(self):
        self.__raw_rows = []
        self.__max_cols = 0

    def add_raw_row(self, raw_row):
        self.__raw_rows.append(raw_row)
        self.__max_cols = max(self.__max_cols, len(raw_row))

    def finalize(self):
        # Create a transpose of the raw rows
        transposed = [''.join(row) for row in zip(*self.__raw_rows)]
        
        self.PATTERN_ROW_ANALYSIS = Analysis(self.__raw_rows, 100)
        self.PATTERN_COL_ANALYSIS = Analysis(transposed,        1)

        return self
    
    def pattern_score(self):
        return sum(x.ANALYSIS_SCORE for x in (self.PATTERN_ROW_ANALYSIS,
                                              self.PATTERN_COL_ANALYSIS))


    def __repr__(self):
        return f"P[{self.PATTERN}]"


class Valley:
    def __init__(self, dataset):
        patterns = []
        current  = None
        for row in dataset:
            if len(row) == 0:
                current = None
                continue
            if current is None:
                current = Pattern()
                patterns.append(current)
            current.add_raw_row(row)
        self.VALLEY_PATTERNS = tuple(p.finalize() for p in patterns)

    def valley_score(self):
        return sum(p.pattern_score() for p in self.VALLEY_PATTERNS)

if __name__ == '__main__':
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample",  sample_data,       405,      -1),
                # (full_data,           1,      -1),
            ]:
        log.info(f"Considering -> {tag=}")
        valley = Valley(dataset)
        found_p1_answer = valley.valley_score()
        log.info(f"{found_p1_answer=} with {expected_p1_answer=}")
        if expected_p1_answer > -1:
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

    log.info(f"Success")


        
