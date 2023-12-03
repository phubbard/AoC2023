from utils import log, load_2d_arrays, safe_insert

# Make a set of known symbols
KNOWN_SYMBOLS = set("+*#$/%&@!?-=<>")


class Grid:
    def __init__(self, array_of_arrays):
        self.GRID_MAX_X = len(array_of_arrays[0])
        self.GRID_MAX_Y = len(array_of_arrays)

        self.GRID_CELLS = {}
        for y in range(self.GRID_MAX_Y):
            previous_cell = None
            for x in range(self.GRID_MAX_X):
                character = array_of_arrays[y][x]
                ordinate  = (x, y)
                cell = Cell(self, character, x, y)
                safe_insert(ordinate, cell, self.GRID_CELLS)
                if previous_cell: previous_cell.cell_set_right(cell)
                previous_cell = cell

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

    def __grid_try_add_neighbor(self, cell, ordinate):
        if ordinate in self.GRID_CELLS:
            cell.cell_add_neighbor(self.GRID_CELLS[ordinate])

class Cell:
    def __init__(self, grid, character, x, y):
        self.CELL_GRID = grid
        self.CELL_CHAR = character
        self.CELL_X    = x
        self.CELL_Y    = y

        self.__cell_right     = None
        self.__cell_neighbors = {}

    def cell_set_right(self, cell):
        self.__cell_right = cell

    def cell_add_neighbor(self, cell):
        self.__cell_neighbors[cell] = True

    def __str__(self) -> str:
        neighbor_chars = [x.CELL_CHAR for x in self.__cell_neighbors.keys()]
        neighbor_string = "".join(neighbor_chars)
        return f"Cell '{self.CELL_CHAR}' at ({self.CELL_X}, {self.CELL_Y}) neighbors:{neighbor_string}"

if __name__ == '__main__':
    sample_data, full_data = load_2d_arrays(3)
    for tag, dataset, expected_answer in [
                ("sample", sample_data,   7),
                ("full",   full_data,   336),
            ]:
        log.info(f"{tag=} {expected_answer=}")
        grid = Grid(dataset)
        for cell in grid.GRID_CELLS.values():
            log.info(cell)
        raise Exception("TODO: Implement me!")
