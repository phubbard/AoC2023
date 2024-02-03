# Dijkstra variations, ahoy!
from utils import log, load_2d_arrays, manhattan_distance
from collections import defaultdict
import heapq

graph = {
    'A': [('B', 2), ('C', 1)],
    'B': [('A', 2), ('C', 4), ('D', 3)],
    'C': [('A', 1), ('B', 4), ('E', 2)],
    'E': [('C', 2), ('D', 1), ('F', 4)],
    'D': [('B', 3), ('E', 1), ('F', 2)],
    'F': [('D', 2), ('E', 4)]

}


def dijkstra(graph, start):
    result_map = defaultdict(lambda: float('inf'))
    result_map[start] = 0

    visited = set()

    queue = [(0, start)]

    while queue:
        weight, v = heapq.heappop(queue)
        visited.add(v)

        for u, w in graph[v]:
            if u not in visited:
                result_map[u] = min(w + weight, result_map[u])
                heapq.heappush(queue, [w + weight, u])

    return result_map



def to_adjacency(input_map: list) -> dict:
    # Given a 2D map, return an adjacency list.
    # The map is a list of lists of integers.
    # Each integer is the node/vertex cost/weight.
    # Nodes are named by their coordinates eg (row, col).
    # The map is a square.
    # The adjacency list is a dictionary of lists.
    # Each vertex is adjacent to at most 4 neighbors.
    adjacency = {}

    for row_idx, row in enumerate(input_map):
        for col_idx, col in enumerate(row):
            node_name = (row_idx, col_idx)
            adjacency[node_name] = []

            # left
            if col_idx > 0:
                adjacency[node_name].append(((row_idx, col_idx - 1), int(input_map[row_idx][col_idx - 1])))
            # right
            if col_idx < len(row) - 1:
                adjacency[node_name].append(((row_idx, col_idx + 1), int(input_map[row_idx][col_idx + 1])))
            # up
            if row_idx > 0:
                adjacency[node_name].append(((row_idx - 1, col_idx), int(input_map[row_idx - 1][col_idx])))
            # down
            if row_idx < len(input_map) - 1:
                adjacency[node_name].append(((row_idx + 1, col_idx), int(input_map[row_idx + 1][col_idx])))

    return adjacency


if __name__ == '__main__':
    sample, full = load_2d_arrays(17)
    print(sample)
    a = to_adjacency(sample)
    pass

    print(dijkstra(a, (0, 0)))