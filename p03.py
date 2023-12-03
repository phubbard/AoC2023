from utils import log, load_2d_arrays


def up(row, col, data):
    if row <= 0:
        return None
    return data[row - 1][col]


def down(row, col, data):
    if row >= len(data) - 1:
        return None
    return data[row + 1][col]


def left(row, col, data):
    if col <= 0:
        return None
    return data[row][col - 1]


def right(row, col, data):
    if col >= len(data[0]) - 1:
        return None
    return data[row][col + 1]


def up_left(row, col, data):
    if row <= 0 or col <= 0:
        return None
    return data[row - 1][col - 1]


def up_right(row, col, data):
    if row <= 0 or col >= len(data[0]) - 1:
        return None
    return data[row - 1][col + 1]


def down_left(row, col, data):
    if row >= len(data) - 1 or col <= 0:
        return None
    return data[row + 1][col - 1]


def down_right(row, col, data):
    if row >= len(data) - 1 or col >= len(data[0]) - 1:
        return None
    return data[row + 1][col + 1]


def get_neighbors(row, col, data):
    return [
        up(row, col, data), down(row, col, data),
        left(row, col, data), right(row, col, data),
        up_left(row, col, data), up_right(row, col, data),
        down_left(row, col, data), down_right(row, col, data)
    ]




if __name__ == '__main__':
    sample, full = load_2d_arrays(3)
    log.info(f"{sample=}")
