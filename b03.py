from utils import log, load_2d_arrays


if __name__ == '__main__':
    sample, full = load_2d_arrays(3)
    log.info(f"{sample=}")
