from utils import get_data_lines, log


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(6)
    for dataset, expected_p1_answer, expected_p2_answer in [
        (sample_data,      -1,      -1),
        (full_data,        -1,      -1),
    ]:
        found_p1_answer = 1
        log.info(f"{expected_p1_answer=} {found_p1_answer=}")
        assert expected_p1_answer == found_p1_answer

    log.info(f"Success")
