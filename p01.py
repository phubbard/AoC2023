# pfh updated filenaming - zero pad the data, use p prefix for my code
# anticipating files from brad and chris

import logging
from utils import get_data_lines, get_data_as_lines


logging.basicConfig(level=logging.DEBUG, format='%(pathname)s(%(lineno)s): %(levelname)s %(message)s')
log = logging.getLogger()


def parse_words_to_numbers(data: list) -> list:
    # given a list of strings with overlapping number words, parse into ordered list of numbers
    # EG eightwothree -> [8, 2, 3]
    search_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    reversed_search_strings = search_strings[::-1]
    best_match = -1
    for word in search_strings:
        loc = word.find(data)




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


    # log.info(f"Part two: {process_data(p2_data)=}")

