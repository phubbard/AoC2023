from utils import get_data_lines, log


class Network:
    def __init__(self):
        self.__nodes = {}

    def add_node(self, assignment_string):
        tag_me, directions = assignment_string.split(' = ')
        tag_left, tag_right = directions.replace('(', '').replace(')', '').split(', ')
        node = Node(tag_me, tag_left, tag_right)
        self.__nodes[tag_me] = node

    def crosslink(self):
        for node in self.__nodes.values():
            left  = self.__nodes[node.NODE_TAG_LEFT]
            right = self.__nodes[node.NODE_TAG_RIGHT]
            node.crosslink_nodes(left, right)


class Node:
    def __init__(self, tag_me, tag_left, tag_right):
        self.NODE_TAG_me    = tag_me
        self.NODE_TAG_LEFT  = tag_left
        self.NODE_TAG_RIGHT = tag_right

    def crosslink_nodes(self, left, right):
        self.NODE_LEFT  = left
        self.NODE_RIGHT = right

if __name__ == '__main__':
    sample_data, full_data = get_data_lines(8)
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,      -1,      -1),
                ("full",     full_data,      -1,      -1),
            ]:
        log.info(f"Considering {tag=}")
        network = Network()
        directions = None
        for line in dataset:
            if directions is None:
                directions = line
            elif len(line) > 0:
                network.add_node(line)
        network.crosslink()
            
    log.info(f"Success")
