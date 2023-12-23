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

    def locate(self, tag):
        return self.__nodes[tag]
    
    def get_nodes(self):
        return self.__nodes.values()


class Node:
    def __init__(self, tag_me, tag_left, tag_right):
        self.NODE_TAG_me    = tag_me
        self.NODE_TAG_LEFT  = tag_left
        self.NODE_TAG_RIGHT = tag_right

        # if self.NODE_TAG_me.endswith('Z'):
        #     if self.NODE_TAG_LEFT  != self.NODE_TAG_me: raise Exception(f"Invalid node: {self.NODE_TAG_me=}")
        #     if self.NODE_TAG_RIGHT != self.NODE_TAG_me: raise Exception(f"Invalid node: {self.NODE_TAG_me=}")

    def crosslink_nodes(self, left, right):
        self.NODE_LEFT  = left
        self.NODE_RIGHT = right


class Journey:
    def __init__(self, network):
        self.__network = network
        self.__cursor  = [n for n in network.get_nodes() if n.NODE_TAG_me.endswith('A')]

    def take_step(self, direction):
        new_cursor = []
        for node in self.__cursor:
            if   direction == 'L': new_cursor.append(node.NODE_LEFT)
            elif direction == 'R': new_cursor.append(node.NODE_RIGHT)
            else: raise Exception(f"Unknown direction: {direction}")
        self.__cursor = new_cursor

    def is_terminal(self):
        for node in self.__cursor:
            if not node.NODE_TAG_me.endswith('Z'): return False
        return True


second_data = \
"""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".split('\n')

third_data = \
"""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".split('\n')


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(8)
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       2,      -1),
                ("second", second_data,       6,      -1),
                ("third",   third_data,      -1,       6),
                ("full",     full_data,   13301,       2),
            ]:
        log.info(f"Considering {tag=}")
        network = Network()
        directions = None
        for line in dataset:
            # log.info(f"Considering {line=}")
            if directions is None:
                directions = line
            elif len(line) > 0:
                network.add_node(line)
        network.crosslink()

        if expected_p1_answer > 0:
            log.info(f"Starting traversal given {directions=}")
            steps = 0
            current_node = network.locate('AAA')
            target_node  = network.locate('ZZZ')
            index = 0
            while current_node != target_node:
                steps += 1
                direction = directions[index]
                index = (index + 1) % len(directions)
                # log.info(f"{steps=} {direction=} {current_node.NODE_TAG_me=} {current_node.NODE_TAG_LEFT=} {current_node.NODE_TAG_RIGHT=}")
                if   direction == 'L': current_node = current_node.NODE_LEFT
                elif direction == 'R': current_node = current_node.NODE_RIGHT
                else: raise Exception(f"Unknown direction: {direction}")
            log.info(f"{steps=} with {expected_p1_answer=}")
            assert steps == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        if expected_p2_answer > 0:
            log.info(f"Starting part two...")
            journey = Journey(network)
            steps = 0
            while not journey.is_terminal():
                steps += 1
                direction = directions[index]
                index = (index + 1) % len(directions)
                journey.take_step(direction)    

            log.info(f"{steps=} with {expected_p2_answer=}")
            assert steps == expected_p2_answer
        else:
            log.info(f"Skipping part two")

    log.info(f"Success")
