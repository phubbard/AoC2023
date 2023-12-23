
from itertools import combinations

from utils import get_data_lines, log




class Galaxy:
    def __init__(self, row, column):
        self.GALAXY_ROW    = row
        self.GALAXY_COLUMN = column

    def __repr__(self):
        return f"G[{self.GALAXY_ROW},{self.GALAXY_COLUMN}]"


class Space:
    def __init__(self):
        self.__space_galaxies   = {} # (row, column) -> galaxy
        self.__space_rows       = {} # row number -> list of galaxies
        self.__space_columns    = {} # column number -> list of galaxies
        self.__space_max_column = 0
        self.__space_max_row    = 0

    def add_space(self, row, column, isGalaxy):
        self.__space_max_column = max(self.__space_max_column, column)
        self.__space_max_row    = max(self.__space_max_row,    row)

        coda = []
        if isGalaxy:
            galaxy = Galaxy(row, column)
            self.__space_galaxies[(row, column)] = galaxy
            coda.append(galaxy)
        self.__space_rows[row]       = self.__space_rows.get(row, [])       + coda
        self.__space_columns[column] = self.__space_columns.get(column, []) + coda

    def grow_space(self):
        delta = 0.5

        for column in range(self.__space_max_column + 1):
            if len(self.__space_columns[column]) > 0: continue
            self.__space_columns[column + delta] = []
        self.__space_columns = {c: self.__space_columns[c] for c in sorted(self.__space_columns.keys())}
        
        for row in range(self.__space_max_row + 1):
            if len(self.__space_rows[row]) > 0: continue
            self.__space_rows[row + delta] = []
        self.__space_rows = {r: self.__space_rows[r] for r in sorted(self.__space_rows.keys())}

        log.info(f"Now cols are {self.__space_columns.keys()}")
        log.info(f"Now rows are {self.__space_rows.keys()}")

    def locate_galaxy(self, row, column):
        return self.__space_galaxies[(row, column)]
    
    def __count_steps(self, keys, start, end):
        if start == end: return 0
        smallest = min(start, end)
        largest  = max(start, end)
        betwixt  = [k for k in keys if smallest < k < largest]
        return 1 + len(betwixt)

    def get_galaxies(self):
        return self.__space_galaxies.values()

    def get_distance(self, galaxy_a, galaxy_b):
        return 0 + \
            self.__count_steps(self.__space_rows.keys(),    galaxy_a.GALAXY_ROW,    galaxy_b.GALAXY_ROW) + \
            self.__count_steps(self.__space_columns.keys(), galaxy_a.GALAXY_COLUMN, galaxy_b.GALAXY_COLUMN)        


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(11)
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       374,       -1),
                ("full",     full_data,   9545480,       -1),
            ]:
        
        space = Space()

        log.info(f"Considering {tag=}")
        if expected_p1_answer > 0:
            for row, line in enumerate(dataset):
                for column, char in enumerate(line):
                    space.add_space(row, column, char == '#')
            space.grow_space()

            pairs = list(combinations(space.get_galaxies(), 2))
            found_p1_answer = 0
            for pair in pairs:
                distance = space.get_distance(pair[0], pair[1])
                found_p1_answer += distance
                # log.info(f"Distance from {pair[0]} to {pair[1]} is {space.get_distance(pair[0], pair[1])}")

            log.info(f"{found_p1_answer=} with {expected_p1_answer=}")
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        if expected_p2_answer > 0:
            found_p2_answer = 3333
            log.info(f"Starting part two...")
            log.info(f"{found_p2_answer=} with {expected_p2_answer=}")
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")

    log.info(f"Success")