from utils import get_data_lines, log

if __name__ == '__main__':

    sample_data, full_data = get_data_lines('12')

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       -1,      -1),
                ("full",   full_data,         -1,      -1),
            ]:
        log.info(f"Considering -> {tag}")

        found_p1_answer = 0
        log.info(f"Steps: {found_p1_answer=} with {expected_p1_answer=}")
        if expected_p1_answer > -1:
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        found_p2_answer = 0
        log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
        if expected_p2_answer > -1:
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")


