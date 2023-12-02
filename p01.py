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

def parse_words_to_numbers(data: list) -> list:
    # given a list of strings with overlapping number words, parse into ordered list of numbers
    # EG eightwothree -> [8, 2, 3]



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
    data, full_data = get_data_lines(1)
    log.info(f"Sample: {process_data(data)=}")
    log.info(f"Full: {process_data(full_data)=}")
