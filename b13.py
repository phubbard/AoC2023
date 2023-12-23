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
        
        self.PATTERN_ROW_VIEW = tuple(self.__raw_rows)
        self.PATTERN_COL_VIEW = tuple(transposed)

        log.info(f"Pattern row view is...")
        for row in self.PATTERN_ROW_VIEW: log.info(f"  {row}")

        log.info(f"Column row view is...")
        for row in self.PATTERN_COL_VIEW: log.info(f"  {row}")

        return self

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

if __name__ == '__main__':
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample",  sample_data,       405,      -1),
                # (full_data,           1,      -1),
            ]:
        log.info(f"Considering -> {tag=}")
        valley = Valley(dataset)

    log.info(f"Success")


        
