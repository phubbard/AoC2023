# pfh updated filenaming - zero pad the data, use p prefix for my code
# anticipating files from brad and chris

import logging
from utils import get_data_lines

logging.basicConfig(level=logging.DEBUG, format='%(pathname)s(%(lineno)s): %(levelname)s %(message)s')
log = logging.getLogger()

part_two = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

number_tuples = [
    (1, 'one'),
    (2, 'two'),
    (3, 'three'),
    (4, 'four'),
    (5, 'five'),
    (6, 'six'),
    (7, 'seven'),
    (8, 'eight'),
    (9, 'nine'),
    ]

def find_first_number(line: str) -> int:
    if len(line) == 0: raise Exception("Not Found")
    for integer, spelled in number_tuples:
        if line.startswith(str(integer)): return integer
        if line.startswith(spelled): return integer
    return find_first_number(line[1:])


def reverse_string(line: str) -> str:
    return ''.join(reversed(line))

def find_last_number(line: str) -> int:
    if len(line) == 0: raise Exception("Not Found")
    reversed_line = reverse_string(line)
    for integer, spelled in number_tuples:
        reverse_spelled = reverse_string(spelled)
        log.info(f"  Now seeking -> {spelled=} aka {reverse_spelled} in {reversed_line}")
        if reversed_line.startswith(str(integer)): return integer
        if reversed_line.startswith(reverse_spelled): return integer
    return find_last_number(line[:-1])





if __name__ == '__main__':
    for line in part_two.split('\n'):
        if len(line) == 0:
            log.info("Skipping zero lenggh line")
            continue
        log.info(f"considering: {line=}")
        first_num = find_first_number(line)
        log.info(f"  {first_num=}")
        last_num = find_last_number(line)
        log.info(f"  {last_num=}")

