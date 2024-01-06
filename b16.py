
from utils import load_2d_arrays, blog

import os


def safe_dictionary_insert(key, value, dictionary):
    if key in dictionary: raise Exception(f"Key {key} already in dictionary")
    dictionary[key] = value
    return value


class Grid:
    def __init__(self, data: list):
        self.GRID_CONTENTS = tuple((tuple(row) for row in data))
        self.GRID_HEIGHT   = len(data)
        self.GRID_WIDTH    = len(data[0])

    def __str__(self):
        return "\n".join(["".join(row) for row in self.GRID_CONTENTS])


if __name__ == '__main__':

    day_number = 16

    sample_data, full_data = load_2d_arrays(day_number)

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,      -1),
                ("real",   full_data,         -1,      -1),
            ]:
        blog(f"Considering -> {tag}")

        grid = Grid(dataset)
        blog(f"grid.GRID_CONTENTS=", multiline=str(grid))

        found_answer_p1 = 0
        blog(f"expected_p1_answer={expected_p1_answer} and found_answer_p1={found_answer_p1}")
        if expected_p1_answer > -1:
            assert found_answer_p1 == expected_p1_answer
        else:
            blog(f"Skipping part one")

        found_answer_p2 = 0
        blog(f"expected_p2_answer={expected_p2_answer} and found_answer_p2={found_answer_p2}")
        if expected_p2_answer > -1:
            assert found_answer_p2 == expected_p2_answer
        else:
            blog(f"Skipping part two")


    blog(f"Success")

