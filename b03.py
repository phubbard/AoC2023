from utils import log, load_2d_arrays, safe_insert

# Make a set of known symbols
KNOWN_SYMBOLS = set("+*#$/%&@!?-=<>")

GEAR_CHARACTER = '*'

DIGITS = set("0123456789")

class Grid:
    def __init__(self, array_of_arrays):
        self.GRID_MAX_X = len(array_of_arrays[0])
        self.GRID_MAX_Y = len(array_of_arrays)

        def _construct_cells():
            """
            Constructs and returns a dictionary of cells based on the given array of arrays.

            Returns:
                dict: A dictionary of cells, where the keys are the cell coordinates and the values are the Cell objects.
            """
            rv = {}
            for y in range(self.GRID_MAX_Y):
                previous_cell = None
                for x in range(self.GRID_MAX_X):
                    character = array_of_arrays[y][x]
                    ordinate  = (x, y)

                    cell = Cell(character, x, y)
                    safe_insert(ordinate, cell, rv)
                    if previous_cell: previous_cell.cell_set_right(cell)
                    previous_cell = cell
            return rv
        self.GRID_CELLS = _construct_cells()

        def _associate_cell_neighbors():
            """
            Associates each cell with its neighbors.
            """
            for x in range(self.GRID_MAX_X):
                for y in range(self.GRID_MAX_Y):
                    cell = self.GRID_CELLS[(x, y)]
                    self.__grid_try_add_neighbor(cell, (x-1, y-1))
                    self.__grid_try_add_neighbor(cell, (x-0, y-1))
                    self.__grid_try_add_neighbor(cell, (x+1, y-1))
                    self.__grid_try_add_neighbor(cell, (x-1, y-0))
                    self.__grid_try_add_neighbor(cell, (x+1, y-0))
                    self.__grid_try_add_neighbor(cell, (x-1, y+1))
                    self.__grid_try_add_neighbor(cell, (x-0, y+1))
                    self.__grid_try_add_neighbor(cell, (x+1, y+1))
            
            for cell in self.GRID_CELLS.values(): cell.cell_freeze()
        _associate_cell_neighbors()

        def _build_numbers():
            """
            Builds a set of Number objects based on the GRID_CELLS.

            Note that this relies on order of construction of cells, which is
            guaranteed by the order of the input data.

            Returns:
                frozenset: A frozenset containing the Number objects.
            """
            numbers = set()
            for cell in self.GRID_CELLS.values():
                if not cell.CELL_CHAR in DIGITS: continue
                # assure that the cell isn't already part of an existing number
                if any([cell in n.NUMBER_CELLS for n in numbers]): continue
                numbers.add(Number(cell))
            return frozenset(numbers)
        self.GRID_NUMBERS = _build_numbers()

        def _determine_gears():
            gear_candidates = {}
            gears = []
            for cell in self.GRID_CELLS.values():
                if cell.CELL_CHAR != GEAR_CHARACTER: continue
                # log.info(f"Found gear at {cell}")
                for number in self.GRID_NUMBERS:
                    if cell in number.NUMBER_NEIGHBORS:
                        gc = gear_candidates[cell] = gear_candidates.get(cell, [])
                        gc.append(number)
            for gear_cell, gear_list in gear_candidates.items():
                is_gear = len(gear_list) == 2
                if is_gear:
                    gears.append(Gear(gear_cell, *gear_list))
                # log.info(f"  gear {str(gear_cell)} {is_gear=}")
                if len(gear_list) > 2:
                    log.info(f" SURPRISE! {gear_list=}")
            return frozenset(gears)
        self.GRID_GEARS = _determine_gears()

    def __grid_try_add_neighbor(self, cell, ordinate):
        if ordinate in self.GRID_CELLS:
            cell.cell_add_neighbor(self.GRID_CELLS[ordinate])

class Cell:
    def __init__(self, character, x, y):
        self.CELL_CHAR = character
        self.CELL_X    = x
        self.CELL_Y    = y

        self.__cell_right     = None
        self.__cell_neighbors = {}

    def cell_set_right(self, cell):
        if self.__cell_right:
            raise Exception(f"Cannot set right cell twice: {self} {cell}")
        self.__cell_right = cell

    def cell_freeze(self):
        self.CELL_NEIGHBORS = frozenset(self.__cell_neighbors.keys())
        self.CELL_RIGHT = self.__cell_right
        del self.__cell_neighbors
        del self.__cell_right

    def cell_add_neighbor(self, cell):
        self.__cell_neighbors[cell] = True

    def __str__(self) -> str:
        neighbor_chars = [x.CELL_CHAR for x in self.__cell_neighbors.keys()]
        neighbor_string = "".join(neighbor_chars)
        right_coda = f" right:{self.__cell_right.CELL_CHAR}" if self.__cell_right else ""
        return f"Cell '{self.CELL_CHAR}' at ({self.CELL_X}, {self.CELL_Y}) neighbors:{neighbor_string}{right_coda}"

class Number:
    def __init__(self, first_cell):
        included_cells = set()
        if first_cell.CELL_CHAR not in DIGITS:
            raise Exception(f"Cannot create a Number from a non-digit cell: {first_cell}")
        value = 0
        current_cell = first_cell
        while current_cell and current_cell.CELL_CHAR in DIGITS:
            included_cells.add(current_cell)
            value = value * 10 + int(current_cell.CELL_CHAR)
            current_cell = current_cell.CELL_RIGHT

        neighbor_superset   = {x for cell in included_cells for x in cell.CELL_NEIGHBORS}
        neighbors_pruned    = {x for x in neighbor_superset if x not in included_cells}
        has_symbol_neighbor = any([x.CELL_CHAR in KNOWN_SYMBOLS for x in neighbors_pruned])

        self.NUMBER_VALUE     = value
        self.NUMBER_CELLS     = frozenset(included_cells)
        self.NUMBER_NEIGHBORS = frozenset(neighbors_pruned)
        self.NUMBER_IS_PART   = has_symbol_neighbor

    def __str__(self) -> str:
        return f"Number {self.NUMBER_VALUE} cells:{len(self.NUMBER_CELLS)} neighbors:{len(self.NUMBER_NEIGHBORS)}"

class Gear:
    def __init__(self, cell, number1, number2):
        self.GEAR_CELL    = cell
        self.GEAR_NUMBER1 = number1
        self.GEAR_NUMBER2 = number2
        self.GEAR_RATIO   = number1.NUMBER_VALUE * number2.NUMBER_VALUE

if __name__ == '__main__':
    sample_data, full_data = load_2d_arrays(3)
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,    4361,   467835),
                ("full",   full_data,    522726, 81721933),
            ]:
        log.info(f"{tag=} part number sum expected: {expected_p1_answer=}")
        grid = Grid(dataset)
        # for cell in grid.GRID_CELLS.values(): log.info(cell)
        part_number_sum = 0
        for number in grid.GRID_NUMBERS:
            # log.info(f'{number.NUMBER_VALUE=} {number.NUMBER_IS_PART=}')
            if number.NUMBER_IS_PART: part_number_sum += number.NUMBER_VALUE
        log.info(f"{expected_p1_answer=} {part_number_sum=}")
        assert expected_p1_answer == part_number_sum

        # Sum the gear ratios
        gear_ratio_sum = sum(g.GEAR_RATIO for g in grid.GRID_GEARS)
        log.info(f"{tag=} Gear ratio expected: {expected_p2_answer=} found: {gear_ratio_sum=}")
        assert expected_p2_answer == gear_ratio_sum
    log.info("SUCCESS")
        

## Todo cleanups, that explore vscode features:
##  - [ ] remove grid member of cell
##  - [ ] alter setting of self.GRID_CELLS to assign once and use set
##  - [ ] rewrite number cell symbols as comprehension