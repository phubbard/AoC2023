from utils import log, load_2d_arrays

# Make a set of known symbols
KNOWN_SYMBOLS = set("+*#$/%&@!?-=<>")


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


def valid_neighbors(row, col, data):
    adjacent = get_neighbors(row, col, data)
    valid = True
    if any([x1 in KNOWN_SYMBOLS for x1 in adjacent]):
        valid = False
        log.debug(f"found symbol adjacent at {row=} {col=}")
    return valid


def coalesce_and_score(row, col, data) -> tuple:
    # For a numeric cell, coalesce righthand digits while checking for
    # neighboring cells that are symbols. Returns the row, col, and score
    # pointing to the cell after the last digit.
    valid = True
    digits = 1
    string = data[row][col]
    if not valid_neighbors(row, col, data):
        valid = False

    right_char = right(row, col, data)
    while right_char and right_char.isdigit():
        col += 1
        if not valid_neighbors(row, col, data):
            valid = False
        string += right_char
        digits += 1
        right_char = right(row, col, data)

    if valid:
        score = int(string)
    else:
        score = 0
    return row, col + 1, score


def process_data(data):
    # Given a 2D array of strings, return the sum of all valid numbers
    # that are not adjacent to symbols.
    row = 0
    col = 0
    score = 0
    while row < len(data):
        while col < len(data[row]):
            char = data[row][col]
            if char.isdigit():
                row, col, cell_score = coalesce_and_score(row, col, data)
                score += cell_score
            else:
                col += 1
        row += 1
        col = 0
    return score


if __name__ == '__main__':
    sample, full = load_2d_arrays(3)
    log.info(f"{sample=}")
    log.info(f"{process_data(sample)=}")
