from utils import get_data_lines, log

import time

if __name__ == '__main__':

    sample_data, full_data = get_data_lines('19')

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,               -1),
                # ("raw_s2", raw_12s2_data,     21,           525152),
                # ("full",   full_data,       8180,  620189727003627),
            ]:

        if expected_p1_answer > -1:
            arrangement_count = 0
            for row in dataset:
                log.info(f"Considering -> {row}")
            found_p1_answer = arrangement_count
            log.info(f"Steps: {found_p1_answer=} with {expected_p1_answer=}")
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        if expected_p2_answer > -1:
            prev_time = time.time()
            arrangement_count = 0
            for row in dataset:
                log.info(f"For row -> {row=}")
                curr_time = time.time()

                log.info(f"{curr_time - prev_time}:  found {permutations} permutations for {row}")
                prev_time = curr_time
            found_p2_answer = arrangement_count

            log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")

