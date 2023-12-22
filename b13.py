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


class Grid:
    def __init__(self)
        self.ROWS = []
                
    def add_row(self, row):
        self.ROWS.append(row)



if __name__ == '__main__':
    for dataset, expected_p1_answer, expected_p2_answer in [
                (sample_data,       405,      -1),
                (full_data,           1,      -1),
            ]:
        grids = []
        grid = None
        for line in dataset:
            if line == "":
                grid = None
            else:
                if grid is None:
                    grid = Grid()
                    grids.append(grid)
                grid.add_row(line)
            pass


    log.info(f"Success")


        
