
from utils import get_data_lines, log, get_data_as_lines


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


def find_zzz(tree, instructions) -> int:
    steps = 0
    root = 'AAA'

    while root != 'ZZZ':
        steps += 1
        instruction = instructions[((steps - 1) % len(instructions))]
        root = one_step(instruction, root, tree)
        if steps % 100000 == 0:
            log.info(f"Step {steps} - root is {root}")

    log.info(f"Found ZZZ in {steps} steps")
    return steps


if __name__ == '__main__':
    sample, full = get_data_lines(8)
    instr, tree = parse_datafile(sample)
    assert find_zzz(tree, instr) == 2

    samp_two = get_data_as_lines(8, 's2')
    instr, tree = parse_datafile(samp_two)
    assert find_zzz(tree, instr) == 6

    instr, tree = parse_datafile(full)
    find_zzz(tree, instr)

