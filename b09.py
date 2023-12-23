from utils import get_data_lines, log

DOESNT_WORK

sample_data = \
"""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def predict_next_number(numbers):
    first_number_list = numbers[:-1]
    second_number_list = numbers[1:]
    delta_list = [s - f for f, s in zip(first_number_list, second_number_list)]


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(9)
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,       -1),
            ]:
        
        log.info(f"Considering {tag=}")
        if expected_p1_answer > 0:
            found_p1_answer = 3333
            log.info(f"{found_p1_answer=} with {expected_p1_answer=}")
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        if expected_p2_answer > 0:
            found_p2_answer = 3333
            log.info(f"Starting part two...")
            log.info(f"{found_p2_answer=} with {expected_p2_answer=}")
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")

    log.info(f"Success")
