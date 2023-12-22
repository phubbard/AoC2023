from utils import get_data_lines, log

if __name__ == '__main__':
    sample_data, full_data = get_data_lines(8)
    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,      -1,      -1),
                ("full",     full_data,      -1,      -1),
            ]:
        log.info(f"Considering {tag=}")
    log.info(f"Success")
