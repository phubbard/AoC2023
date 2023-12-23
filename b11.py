
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

    def add_space(self, row, column, is_galaxy):
        self.__space_max_column = max(self.__space_max_column, column)
        self.__space_max_row    = max(self.__space_max_row,    row)

        coda = []
        if is_galaxy:
            galaxy = Galaxy(row, column)
            self.__space_galaxies[(row, column)] = galaxy
            coda.append(galaxy)
        self.__space_rows[row]       = self.__space_rows.get(row, [])       + coda
        self.__space_columns[column] = self.__space_columns.get(column, []) + coda

    def grow_space(self, growth_factor):
        delta = 0.5
        added_count = growth_factor - 1

        for column in range(self.__space_max_column + 1):
            if len(self.__space_columns[column]) > 0: continue
            self.__space_columns[column + delta] = added_count
        self.__space_columns = {c: self.__space_columns[c] for c in sorted(self.__space_columns.keys())}
        
        for row in range(self.__space_max_row + 1):
            if len(self.__space_rows[row]) > 0: continue
            self.__space_rows[row + delta] = added_count
        self.__space_rows = {r: self.__space_rows[r] for r in sorted(self.__space_rows.keys())}

        log.info(f"Now cols are {self.__space_columns.keys()}")
        log.info(f"Now rows are {self.__space_rows.keys()}")

    def locate_galaxy(self, row, column):
        return self.__space_galaxies[(row, column)]
    
    def __count_steps(self, dictionary, start, end):
        if start == end: return 0
        smallest = min(start, end)
        largest  = max(start, end)
        betwixt  = [(k,v) for k,v in dictionary.items() if smallest < k < largest]
        distance = 1
        for k,v in betwixt:
            if isinstance(v, list):  distance += 1
            elif isinstance(v, int): distance += v
            else: raise Exception(f"Unexpected type {type(v)}")
        return distance

    def get_galaxies(self):
        return self.__space_galaxies.values()

    def get_distance(self, galaxy_a, galaxy_b):
        return 0 + \
            self.__count_steps(self.__space_rows,    galaxy_a.GALAXY_ROW,    galaxy_b.GALAXY_ROW) + \
            self.__count_steps(self.__space_columns, galaxy_a.GALAXY_COLUMN, galaxy_b.GALAXY_COLUMN)        


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(11)
    for tag, dataset, growth_factor, expected_p1_answer in [
                ("sample x 1",    sample_data,       2,           374),
                ("sample x 10",   sample_data,      10,          1030),
                ("sample x 1000", sample_data,     100,          8410),
                ("full x 1",        full_data,       2,       9545480),
                ("full x 1M",       full_data, 1000000,  406725732046),
            ]:
        
        space = Space()

        log.info(f"Considering {tag=}")
        if expected_p1_answer > 0:
            for row, line in enumerate(dataset):
                for column, char in enumerate(line):
                    space.add_space(row, column, char == '#')
            space.grow_space(growth_factor)

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

    log.info(f"Success")
