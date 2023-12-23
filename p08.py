from math import lcm
from utils import get_data_lines, log, get_data_as_lines
from functools import reduce


def parse_datafile(datalines):
    instr = datalines[0]
    tree = {}

    for line in datalines[2:]:
        tokens = line.split(' = ')
        name = tokens[0]
        leftright = tokens[1].split(', ')
        left = leftright[0][1:]
        right = leftright[1][:-1]
        log.debug(f"Adding node {name} with left {left} and right {right}")
        tree[name] = [left, right]

    log.info(f"Found {len(instr)} instructions and {len(tree)} nodes")
    return instr, tree


def one_step(direction, nodename, tree):
    log.debug(f"one_step({direction}, {nodename})")
    if direction == 'L':
        return tree[nodename][0]
    else:
        return tree[nodename][1]


def n_steps(n, directions, nodename, tree):
    for _ in range(n):
        nodename = one_step(directions, nodename, tree)
    return nodename


def find_zzz(tree, instructions) -> int:
    steps = 0
    root = 'AAA'

    while root != 'ZZZ':
        steps += 1
        instruction = instructions[((steps - 1) % len(instructions))]
        root = one_step(instruction, root, tree)
        # if steps % 100000 == 0:
        #     log.info(f"Step {steps} - root is {root}")

    log.info(f"Found ZZZ in {steps} steps")
    return steps


def find_z_node(start_name, tree, instructions) -> int:
    # Given a starting node (ending in A), find the min steps to a node ending in Z.
    steps = 0
    root = start_name
    while not root.endswith('Z'):
        steps += 1
        instruction = instructions[((steps - 1) % len(instructions))]
        root = one_step(instruction, root, tree)

    log.info(f"Found Z node {root} in {steps} steps")
    return steps


if __name__ == '__main__':
    sample, full = get_data_lines(8)
    instr, tree = parse_datafile(sample)
    assert find_zzz(tree, instr) == 2

    samp_two = get_data_as_lines(8, 's2')
    instr, tree = parse_datafile(samp_two)
    assert find_zzz(tree, instr) == 6

    instr, tree = parse_datafile(full)
    assert find_zzz(tree, instr) == 13301

    samp_three = get_data_as_lines(8, 's3')
    instr, tree = parse_datafile(samp_three)
    a_keys = [k for k in tree.keys() if k.endswith('A')]
    log.info(f"Found {len(a_keys)} nodes ending in A")
    log.info(a_keys)
    t_lcm = lcm(*[find_z_node(k, tree, instr) for k in a_keys])
    log.info(f"LCM is {t_lcm}")

    instr, tree = parse_datafile(full)
    a_keys = [k for k in tree.keys() if k.endswith('A')]
    log.info(f"Found {len(a_keys)} nodes ending in A")
    log.info(a_keys)
    lengths = [find_z_node(k, tree, instr) for k in a_keys]
    log.info(f"LCM is {lcm(*lengths)}")
