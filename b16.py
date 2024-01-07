
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
CELL_ENERGIZED       = '#'

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

        # blog(f"Calculating beam from ({start_column}, {start_row}) in direction {direction.DIR_NAME}", frameNudge=1)

        cell   = None
        split  = None
        bent   = None
        escape = None
        while True:
            # Skip first cell
            column += direction.DIR_COLUMN_DELTA
            row    += direction.DIR_ROW_DELTA   
            cell = grid.get_cell(column, row)
            # blog(f"   check ({column}, {row}) -> {cell}", frameNudge=1)
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
        self.BEAM_ESCAPE       = escape

    def __str__(self):
        prefix = f"Beam({self.BEAM_START_COLUMN}, {self.BEAM_START_ROW}) {self.BEAM_DIRECTION.DIR_NAME} to ({self.BEAM_END_COLUMN}, {self.BEAM_END_ROW}) "
        if self.BEAM_ESCAPE: postfix = "escaped"
        elif self.BEAM_SPLIT: postfix = f"split to {self.BEAM_SPLIT[0].DIR_NAME} and {self.BEAM_SPLIT[1].DIR_NAME}"
        elif self.BEAM_BENT:  postfix = f"bent to {self.BEAM_BENT.DIR_NAME}"
        return prefix + postfix


class Tracer:
    def __init__(self, grid, beams):
        # First make an array of arrays of spaces, sized according to grid
        energized = [[CELL_SPACE for column in range(grid.GRID_COLUMNS)] for row in range(grid.GRID_ROWS)]

        # Now set to energized all cells that are part of a beam
        for beam in beams.values():
            # blog(f"Processing beam {beam}", frameNudge=1)
            column = beam.BEAM_START_COLUMN
            row    = beam.BEAM_START_ROW
            while (column, row) != (beam.BEAM_END_COLUMN, beam.BEAM_END_ROW):
                # blog(f"Checking ({column}, {row}) for energization", frameNudge=1)
                if 0 <= column < grid.GRID_COLUMNS and 0 <= row < grid.GRID_ROWS:
                    # blog(f"Setting ({column}, {row}) to energized", frameNudge=1)
                    energized[row][column] = CELL_ENERGIZED
                column += beam.BEAM_DIRECTION.DIR_COLUMN_DELTA
                row    += beam.BEAM_DIRECTION.DIR_ROW_DELTA

        # store the array
        self.TRACER_ENERGIZED = energized

    def get_energized_count(self):
        return sum([sum([1 if cell == CELL_ENERGIZED else 0 for cell in row]) for row in self.TRACER_ENERGIZED])
        
    def __str__(self):
        return "\n".join(["".join(row) for row in self.TRACER_ENERGIZED])



if __name__ == '__main__':

    day_number = 16

    sample_data, full_data = load_2d_arrays(day_number)

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       46,      -1),
                ("real",   full_data,       8116,      -1),
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
                where = (beam.BEAM_START_COLUMN, beam.BEAM_START_ROW, beam.BEAM_DIRECTION)
                if where in beams:
                    continue # already processed this beam

                # Create any new beams
                if beam.BEAM_SPLIT:
                    for direction in beam.BEAM_SPLIT:
                        new_beam = Beam(grid, beam.BEAM_END_COLUMN, beam.BEAM_END_ROW, direction)
                        new_beams.append(new_beam)
                elif beam.BEAM_BENT:
                    new_beam = Beam(grid, beam.BEAM_END_COLUMN, beam.BEAM_END_ROW, beam.BEAM_BENT)
                    new_beams.append(new_beam)
                elif beam.BEAM_ESCAPE:
                    pass
                else: raise Exception(f"Unexpected beam state {beam}")

                # record this beam
                beams[where] = beam 
            active_beams = new_beams

        tracer = Tracer(grid, beams)
        found_answer_p1 = tracer.get_energized_count()
        blog(f"RESULT={found_answer_p1}", multiline=str(tracer))

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

