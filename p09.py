from utils import get_data_lines, log


if __name__ == '__main__':
    sample, full = get_data_lines(9)

    sample_data = []
    for line in sample:
        sample_data.append([int(x) for x in line.split()])
    data = []
    for line in full:
        data.append([int(x) for x in line.split()])

    pass