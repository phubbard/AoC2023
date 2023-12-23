from utils import get_data_lines, log




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
