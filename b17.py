
from utils import load_2d_arrays, blog, safe_insert

import os

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


# Whether the next move must be vertical or horizontal
PLANE_VERTICAL   = 'v'
PLANE_HORIZONTAL = 'h'
PLANE_START      = 's'
PLANE_FINISH     = 'f'


class Node:
    def __init__(self, name: str, row: int, column: int, plane: int):
        self.NODE_NAME   = name
        self.NODE_ROW    = row
        self.NODE_COLUMN = column
        self.NODE_PLANE  = plane
        self.__node_working = {} # dict

    def node_neighbor(self, neighbor_name: str, cost: int):
        safe_insert(self.__node_working, neighbor_name, cost)

    def node_freeze(self, builder):
        self.NODE_NEIGHBORS = tuple(builder.make_node(name) for name in self.__node_working)
        del self.__node_working


class Builder:
    def __init__(self):
        self.__working_nodes = {}

    def builder_node(self, row, column, plane):
        node_name = f"{plane}:{row},{column}"
        if node_name not in self.__working_nodes:
            self.__working_nodes[node_name] = Node(node_name, row, column, plane)
        return self.__working_nodes[node_name]
    
    def builder_freeze(self):
        for node in self.__working_nodes.values():
            node.node_freeze(self)
        self.BUILDER_NODES = tuple(self.__working_nodes.values())
        del self.__working_nodes


if __name__ == '__main__':

    day_number = 17

    sample_data, full_data = load_2d_arrays(day_number)

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       46,      51),
                ("real",   full_data,       8116,    8383),
            ]:
        blog(f"Considering -> {tag}")

        grid = Grid(dataset)
        blog(f"grid.GRID_CONTENTS=", multiline=str(grid))

        found_answer_p1 = 99

        blog(f"expected_p1_answer={expected_p1_answer} and found_answer_p1={found_answer_p1}")
        if expected_p1_answer > -1:
            assert found_answer_p1 == expected_p1_answer
        else:
            blog(f"Skipping part one")

        found_answer_p2 = 88
        blog(f"expected_p2_answer={expected_p2_answer} and found_answer_p2={found_answer_p2}")
        if expected_p2_answer > -1:
            assert found_answer_p2 == expected_p2_answer
        else:
            blog(f"Skipping part two")


    blog(f"Success")

