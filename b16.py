
from utils import load_2d_arrays, blog

import os


def safe_dictionary_insert(key, value, dictionary):
    if key in dictionary: raise Exception(f"Key {key} already in dictionary")
    dictionary[key] = value
    return value


class Grid:
    def __init__(self, data: list):
        self.GRID_CONTENTS = tuple((tuple(row) for row in data))
        self.GRID_ROWS     = len(data)
        self.GRID_COLUMNS  = len(data[0])

    def get_cell(self, column: int, row: int):
        if column < 0 or column >= self.GRID_COLUMNS: return None
        if row    < 0 or row    >= self.GRID_ROWS:    return None
        return self.GRID_CONTENTS[row][column]

    def __str__(self):
        return "\n".join(["".join(row) for row in self.GRID_CONTENTS])


CELL_PIPE_VERTICAL   = '|'
CELL_PIPE_HORIZONTAL = '-'
CELL_DIAG_RIGHT      = '\\'
CELL_DIAG_LEFT       = '/'
CELL_SPACE           = '.'

class Direction:
    def __init__(self, name: str,
                 delta_column: int,
                 delta_row: int,
                 splitting_cell: str,
                 clockwise_cell: str,
                 counterclockwise_cell: str,
                 ):
        self.DIR_NAME             = name
        self.DIR_COLUMN_DELTA     = delta_column
        self.DIR_ROW_DELTA        = delta_row
        self.DIR_SPLITTING        = splitting_cell
        self.DIR_CLOCKWISE        = clockwise_cell
        self.DIR_COUNTERCLOCKWISE = counterclockwise_cell

DIR_RIGHT = Direction("right",  1,  0, CELL_PIPE_VERTICAL,  CELL_DIAG_RIGHT, CELL_DIAG_LEFT)
DIR_LEFT  = Direction("left",  -1,  0, CELL_PIPE_VERTICAL,  CELL_DIAG_RIGHT, CELL_DIAG_LEFT)
DIR_UP    = Direction("up",     0, -1, CELL_PIPE_HORIZONTAL, CELL_DIAG_LEFT,  CELL_DIAG_RIGHT)
DIR_DOWN  = Direction("down",   0,  1, CELL_PIPE_HORIZONTAL, CELL_DIAG_LEFT,  CELL_DIAG_RIGHT)

ROTATE_CLOCKWISE = {
    DIR_RIGHT: DIR_DOWN,
    DIR_DOWN:  DIR_LEFT,
    DIR_LEFT:  DIR_UP,
    DIR_UP:    DIR_RIGHT,
}

ROTATE_COUNTERCLOCKWISE = {
    DIR_RIGHT: DIR_UP,
    DIR_UP:    DIR_LEFT,
    DIR_LEFT:  DIR_DOWN,
    DIR_DOWN:  DIR_RIGHT,
}

SPLIT_RESULT = {
    DIR_RIGHT: (DIR_UP, DIR_DOWN),
    DIR_LEFT:  (DIR_UP, DIR_DOWN),
    DIR_UP:    (DIR_LEFT, DIR_RIGHT),
    DIR_DOWN:  (DIR_LEFT, DIR_RIGHT),
}

class Beam:
    def __init__(self,
                 grid: Grid,
                 start_column: int,
                 start_row: int,
                 direction: Direction,
                 ):
        column = start_column
        row    = start_row
        cell   = None
        split  = None
        bent   = None
        escape = None
        while True:
            # Skip first cell
            column += direction.DIR_COLUMN_DELTA
            row    += direction.DIR_ROW_DELTA   
            cell = grid.get_cell(column, row)
            if cell is None: 
                escape = True
                break
            if cell == CELL_SPACE: continue
            if cell == direction.DIR_SPLITTING:
                split = SPLIT_RESULT[direction]    
                break
            if cell == direction.DIR_CLOCKWISE:
                bent = ROTATE_CLOCKWISE[direction]
                break
            if cell == direction.DIR_COUNTERCLOCKWISE:
                bent = ROTATE_COUNTERCLOCKWISE[direction]
                break
            continue

        self.BEAM_START_COLUMN = start_column
        self.BEAM_START_ROW    = start_row
        self.BEAM_DIRECTION    = direction
        self.BEAM_END_COLUMN   = column
        self.BEAM_END_ROW      = row
        self.BEAM_SPLIT        = split
        self.BEAM_BENT         = bent


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

        beams = {} # (start_column, start_row, direction) -> Beam
        first_beam = Beam(grid, -1, 0, DIR_RIGHT)
        active_beams = [first_beam]
        while len(active_beams) > 0:
            new_beams = []
            for beam in active_beams:
                # Create any new beams
                if beam.BEAM_SPLIT:
                    for direction in beam.BEAM_SPLIT:
                        new_beam = Beam(grid, beam.BEAM_START_COLUMN, beam.BEAM_START_ROW, direction)
                        new_beams.append(new_beam)
                elif beam.BEAM_BENT:
                    new_beam = Beam(grid, beam.BEAM_START_COLUMN, beam.BEAM_START_ROW, beam.BEAM_BENT)
                    new_beams.append(new_beam)
                elif beam.BEAM_ESCAPE:
                    pass
                else: raise Exception(f"Unexpected beam state {beam}")

                # record this beam
                where = (beam.BEAM_START_COLUMN, beam.BEAM_START_ROW, beam.BEAM_DIRECTION)
                if not where in beams:
                    beams[where] = beam 
            active_beams = new_beams

        raise Exception(f"TODO after {len(beams)} beams")

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

