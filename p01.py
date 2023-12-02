# pfh updated filenaming - zero pad the data, use p prefix for my code
# anticipating files from brad and chris

import logging
from utils import get_data_lines, get_data_as_lines


logging.basicConfig(level=logging.DEBUG, format='%(pathname)s(%(lineno)s): %(levelname)s %(message)s')
log = logging.getLogger()


# Try the stabbylambda approach
def expand_strings(line: str) -> str:
    remap = [
        {'one': 'one1one'}, {'two': 'two2two'},
        {'three': 'three3three'},
        {'four': 'four4four'},
        {'five': 'five5five'}, {'six': 'six6six'},
        {'seven': 'seven7seven'},
        {'eight': 'eight8eight'},
        {'nine': 'nine9nine'}, {'zero': 'zero0zero'}
    ]

    for idx in range(len(remap)):
        src = list(remap[idx].keys())[0]
        dest = list(remap[idx].values())[0]
        line = line.replace(src, dest)
    return line

    
def process_data(data: list) -> int:
    numbers = []
    for line in data:
        rc = [x1 for x1 in line if x1.isdigit()]
        numbers.append(rc)
        log.debug(f"{line=}")
    a_sum = 0
    for line in numbers:
        first = line[0]
        last = line[-1]
        a_sum += int(f"{first}{last}")
    log.info(a_sum)
    return a_sum


if __name__ == '__main__':
    sample_data = get_data_as_lines(1, 's')
    full_data = get_data_as_lines(1)
    p2_data = get_data_as_lines(1, 'p2')

    log.info(f"Sample: {process_data(sample_data)=}")
    log.info(f"Full: {process_data(full_data)=}")

    p2s = get_data_as_lines(1, 's2')
    rc = []
    for line in p2s:
        rc.append(expand_strings(line))
    log.info(f"Part two sample {process_data(rc)=}")
    # log.info(f"Part two: {process_data(p2_data)=}")

