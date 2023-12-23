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
        self.__network  = network
        self.__cursor   = [n for n in network.get_nodes() if n.NODE_TAG_me.endswith('A')]
        self.__baseline = [None for c in self.__cursor]
        self.__delta    = [0 for c in self.__cursor]
        log.info(f"Starting journey with {len(self.__cursor)=}")

    def single_step(self, direction, steps):
        new_cursor = []
        for index, node in enumerate(self.__cursor):
            if node.NODE_TAG_me.endswith('Z'):
                baseline = self.__baseline[index]
                if baseline is None:
                    self.__baseline[index] = steps
                else:
                    delta = self.__delta[index]
                    if delta == 0:
                        self.__delta[index] = steps - baseline

            if   direction == 'L': new_cursor.append(node.NODE_LEFT)
            elif direction == 'R': new_cursor.append(node.NODE_RIGHT)
            else: raise Exception(f"Unknown direction: {direction}")
        self.__cursor = new_cursor

    def is_resonating(self):
        for delta in self.__delta:
            if delta == 0: return False
        return True
    
    def describe_resonance(self):
        for index, node in enumerate(self.__cursor):
            log.info(f"{index=} {node.NODE_TAG_me=} {self.__baseline[index]=} {self.__delta[index]=}")

    def take_hop(self):
        adjust_index = 0
        adjust_baseline = self.__baseline[adjust_index]
        for index, baseline in enumerate(self.__baseline):
            if baseline < adjust_baseline:
                adjust_index = index
                adjust_baseline = baseline
        new_baseline = adjust_baseline + self.__delta[adjust_index]
        self.__baseline[adjust_index] = new_baseline
        return new_baseline

    def is_terminal(self):
        return len(set(self.__baseline)) == 1

    def snapshot(self):
        return '-'.join(n.NODE_TAG_me for n in self.__cursor)


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
            while not journey.is_resonating():
                direction = directions[index]
                index = (index + 1) % len(directions)
                ss = journey.snapshot()
                if 'Z' in ss: log.info(f"{steps=} {ss=}")
                journey.single_step(direction, steps)
                steps += 1

            journey.describe_resonance()
            laps = 0
            while not journey.is_terminal():
                laps += 1
                steps = journey.take_hop()
                if laps % 1000000 == 0:
                    log.info(f"{laps=} {steps=}")
                    journey.describe_resonance()
            log.info(f"{steps=} with {expected_p2_answer=}")
            assert steps == expected_p2_answer
        else:
            log.info(f"Skipping part two")

    log.info(f"Success")
