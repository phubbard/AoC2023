
from itertools import permutations, combinations_with_replacement
import logging

logging.basicConfig(level=logging.INFO, format='%(pathname)s(%(lineno)s): %(levelname)s %(message)s')
log = logging.getLogger()


def find_permutations(input_chars, length=8):
    return permutations(input_chars, r=length)


def find_combinations(input_chars, length=8):
    return combinations_with_replacement(input_chars, r=length)


def find_combinations_from_scratch(input_chars, length=8):
    rc = []
    for i in range(length):
        for j in range(length):
            rc += f'{input_chars[i]}{input_chars[j]}'
    return rc


def clean_lines(input_lines):
    # Remove newlines and such that fuck up the parser
    return [x.strip() for x in input_lines]


def manhattan_distance(p1, p2):
    return sum([abs(p1[x] - p2[x]) for x in range(len(p1))])


def make_2d_array(num_rows, num_cols, fill=0):
    # Create and allocate a 2D array. Copypasta from SO with edits.
    return [[fill] * num_cols for _ in range(num_rows)]


def load_2d_arrays(problem_number):
    # some of these encode a map as a 2D array, so we should be able to reuse this.
    sample, full = get_data_lines(problem_number)

    num_rows = len(sample)
    num_cols = len(sample[0])
    data = make_2d_array(num_rows, num_cols)
    for row, line in enumerate(sample):
        for col, char in enumerate(line):
            data[row][col] = char
    sample_2d = data

    num_rows = len(full)
    num_cols = len(full[0])
    data = make_2d_array(num_rows, num_cols)
    for row, line in enumerate(full):
        for col, char in enumerate(line):
            data[row][col] = char
    full_2d = data

    return sample_2d, full_2d


def get_column(data, col_idx):
    # No way to extract a column without numpy so Just Deal.
    return [row[col_idx] for row in data]


def get_data_as_lines(problem_number: int, suffix: str = '') -> list:
    zero_padded = zero_pad(problem_number)
    filename = f'./data/{zero_padded}{suffix}.txt'
    return clean_lines(open(filename, 'r').readlines())


def zero_pad(number, digits=2):
    return f"{number:0{digits}}"


def get_data_lines(problem_number):
    # Return a tuple of (sample data, full data)
    # Based on the problem number. Normal
    # pattern is to have line-specific parsers that operate on the return from this.
    zero_padded = f"{problem_number:02}"
    sample_file = f'./data/{zero_padded}s.txt'
    data_file = f'./data/{zero_padded}.txt'

    sample_data = clean_lines(open(f'./data/{zero_padded}s.txt', 'r').readlines())
    full_data = clean_lines(open(f'./data/{zero_padded}.txt', 'r').readlines())
    return (sample_data, full_data)


def draw_coordinate_line_closed(tuple_from, tuple_to):
    """Return a list of integer points between two tuples, including the endpoints.

    At the time of this writing, this does not support diagonals: only one dimension
    of endpoint coordinates is allowed to differ between from and to.

    """
    assert len(tuple_from) == len(tuple_to)

    list_delta = []
    for x in range(len(tuple_from)):
        value_from = tuple_from[x]
        value_to   = tuple_to[x]
        assert isinstance(value_from, int)
        assert isinstance(value_to,   int)

        list_delta.append(value_to - value_from)

    count_nonzero_dimensions = len([x for x in list_delta if x != 0])
    assert count_nonzero_dimensions < 2

    raise Exception("This was never finished.  Next time!")


def safe_insert(key, value, dictish):
    """If and only if the key is not present, insert it."""
    if key in dictish:
        existing = dictish[key]
        raise Exception(f"Cannot supplant at {str(key)=} ...\n  EXISTING {str(existing)} \n  NEW      {str(value)}")
    dictish[key] = value
    return value


# From 2022 day 12 - Dijkstra's algorithm and related code
def is_adjacent(source: int, dest: int, elevation_map) -> int:
    # The adjacency matrix creation needs to know if two vertices are connected or not. This answers it.
    num_cols = len(elevation_map[0])
    source_row, source_col = divmod(source, num_cols)
    dest_row, dest_col = divmod(dest, num_cols)
    source_height = elevation_map[source_row][source_col]
    dest_height = elevation_map[dest_row][dest_col]

    if source == dest:
        return 0  # Zeros on the diagonal by definition
    # For part one, you can step up one or down many. For part two, only up or down one.
    # if (dest_height - source_height) > 1:
    if (source_height - dest_height) > 1:
        return 0

    if source_row == dest_row:
        if abs(source_col - dest_col) > 1:
            return 0  # More than one away
        # nb we already checked for height diff above
        return 1
    if abs(source_row - dest_row) > 1:
        return 0
    if source_col == dest_col:
        return 1

    # All that and checking delta H and distance might be a lot simpler. Ahh well.
    return 0


def to_adjacency(map):
    # For each cell/vertex, the LRUD cells are adjacent if the height difference is <= 1.
    # For N cells, the matrix is NxN, symmetric about the diagonal, zeros on diagonal
    num_cols = len(map[0])
    col_zero = [row[0] for row in map]
    num_rows = len(col_zero)
    num_cells = num_rows * num_cols
    print(f"{num_cols} cols and {num_rows} rows == {num_cells}^2 in adjacency matrix")
    # Avert your eyes.
    zero_row = [0 for x in range(num_cells)]
    adj_matrix = [deepcopy(zero_row) for y in range(num_cells)]

    for row_idx in range(num_cells):
        for col_idx in range(num_cells):
            adj_matrix[row_idx][col_idx] = is_adjacent(row_idx, col_idx, map)

    return adj_matrix


##########################################################
#

class Graph:
    # Code from https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
    # Python program for Dijkstra's single source shortest path algorithm. The program is
    # for adjacency matrix representation of the graph.
    def __init__(self, vertices):
        self.V = len(vertices[0])
        self.graph = vertices

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):

        # Initialize minimum distance for next node
        min = 1e7

        # Search not nearest vertex not in the
        # shortest path tree
        min_index = 0
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                        sptSet[v] == False and
                        dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]

        # self.printSolution(dist)
        return dist

# This code is contributed by Divyanshu Mehta

#  END
#
##########################################################
