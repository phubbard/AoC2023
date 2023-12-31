# pfh updated filenaming - zero pad the data, use p prefix for my code
# anticipating files from brad and chris

import logging
from utils import get_data_lines, zero_pad

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
        # log.info(f"  Now seeking -> {spelled=} aka {reverse_spelled} in {reversed_line}")
        if reversed_line.startswith(str(integer)): return integer
        if reversed_line.startswith(reverse_spelled): return integer
    return find_last_number(line[:-1])

PROBLEM = zero_pad(1)

if __name__ == '__main__':

    for input_lines, expectation in [
        (get_data_as_lines(PROBLEM, 's'),     142),
        (get_data_as_lines(PROBLEM, ''),    54081),
        (get_data_as_lines(PROBLEM, 's2'),    281),
        (get_data_as_lines(PROBLEM, ''),    54649),
    ]:
        final_sum = 0
        sample_data, full_data = get_data_lines(1)
        for line in full_data:
            if len(line) == 0:
                log.info("Skipping zero lengh line")
                continue
            log.info(f"considering: {line=}")
            first_num = find_first_number(line)
            # log.info(f"  {first_num=}")
            last_num = find_last_number(line)
            # log.info(f"  {last_num=}")
            addend = first_num * 10 + last_num
            log.info("  adding {addend=}")
            final_sum += addend
        log.info(f"  {final_sum=}")
        if final_sum != expectation:
            log.error(f"Expected {expectation=}, got {final_sum=}")
    

