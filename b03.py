from utils import log, load_2d_arrays, safe_insert

# Make a set of known symbols
KNOWN_SYMBOLS = set("+*#$/%&@!?-=<>")

GEAR_CHARACTER = '*'

DIGITS = set("0123456789")

class Grid:
    def __init__(self, array_of_arrays):
        self.GRID_MAX_X = len(array_of_arrays[0])
        self.GRID_MAX_Y = len(array_of_arrays)

        # Construct Cells
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

        # Associate Cell neighbors
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
        _associate_cell_neighbors()

        # Build Numbers
        #  Note that this relies on order of construction of cells, which is
        #  guaranteed by the order of the input data.
        numbers = set()
        for cell in self.GRID_CELLS.values():
            if not cell.CELL_CHAR in DIGITS: continue
            # assure that the cell isn't already part of an existing number
            if any([cell in n.NUMBER_INCLUDED_CELLS for n in numbers]): continue
            numbers.add(Number(cell))
        self.GRID_NUMBERS = frozenset(numbers)

        # Determine gears
        log.info("Determining gears")
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
        self.GRID_GEARS = frozenset(gears)

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
        self.__cell_right = cell

    def cell_get_right(self):
        return self.__cell_right

    def cell_add_neighbor(self, cell):
        self.__cell_neighbors[cell] = True

    def cell_get_neighbors(self):
        return self.__cell_neighbors.keys()

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
            current_cell = current_cell.cell_get_right()

        number_neighbors = set()

        for cell in included_cells:
            for neighbor in cell.cell_get_neighbors():
                number_neighbors.add(neighbor)
        for cell in included_cells:
            if cell in number_neighbors:            
                number_neighbors.remove(cell)

        # Determine if any of the included cells have neighbors that are symbols
        has_symbol_neighbor = False
        for neighbor in number_neighbors:
            if neighbor.CELL_CHAR in KNOWN_SYMBOLS:
                has_symbol_neighbor = True

        self.NUMBER_VALUE          = value
        self.NUMBER_NEIGHBORS      = frozenset(number_neighbors)
        self.NUMBER_INCLUDED_CELLS = frozenset(included_cells)
        self.NUMBER_IS_PART        = has_symbol_neighbor

    def __str__(self) -> str:
        return f"Number {self.NUMBER_VALUE} cells:{len(self.NUMBER_INCLUDED_CELLS)} neighbors:{len(self.NUMBER_NEIGHBORS)}"

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