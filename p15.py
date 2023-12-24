from utils import get_data_lines, log


def aoc_hash(input: str) -> int:
    value = 0
    for char in input:
        value += ord(char)
        value *= 17
        value = value % 256
    return value


if __name__ == '__main__':
    log.setLevel('DEBUG')
    assert(aoc_hash('HASH') == 52)

    sample, full = get_data_lines('15')

    for dataline in sample:
        log.info(f'{sum([aoc_hash(x) for x in dataline.split(',')])=}')

    for dataline in full:
        log.info(f'{sum([aoc_hash(x) for x in dataline.split(',')])=}')