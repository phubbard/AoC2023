
from utils import get_data_lines, log

tree = []


def parse_nodeline(line) -> {}:
    tokens = line.split(' = ')
    name = tokens[0]
    leftright = tokens[1].split(', ')
    left = leftright[0][1:]
    right = leftright[1][:-1]
    rc = {name: (left, right)}
    return rc


def parse_datafile(datalines):
    global tree
    instr = datalines[0]
    log.info(f"Found {len(instr)} instructions")

    for line in datalines[2:]:
        node = parse_nodeline(line)
        log.debug(f"Adding node {node}")
        tree.append(node)
    return instr, tree


def find_zzz(root) -> int:
    steps = 0


if __name__ == '__main__':
    sample, full = get_data_lines(8)
    parse_datafile(sample)
    parse_datafile(full)
