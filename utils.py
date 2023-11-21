
from itertools import permutations, combinations, combinations_with_replacement


def find_permutations(input_chars, length=8):
    return permutations(input_chars, r=length)


def find_combinations(input_chars, length=8):
    return combinations_with_replacement(input_chars, r=length)


def find_combinations_from_scratch(input_chars, length=8):
    rc = []
    for i in range(length):
        for j in range(length):
            rc += f'{input_chars[i]}{input_chars[j]}'
    return rc


def clean_lines(input_lines):
    # Remove newlines and such that fuck up the parser
    return [x.strip() for x in input_lines]


def make_2d_array(num_rows, num_cols, fill=0):
    # Create and allocate a 2D array. Copypasta from SO with edits.
    return [[fill] * num_cols for _ in range(num_rows)]


def load_2d_arrays(problem_number):
    # some of these encode a map as a 2D array, so we should be able to reuse this.
    sample, full = get_data_lines(problem_number)

    num_rows = len(sample)
    num_cols = len(sample[0])
    data = make_2d_array(num_rows, num_cols)
    for row, line in enumerate(sample):
        for col, char in enumerate(line):
            data[row][col] = int(char)
    sample_2d = data

    num_rows = len(full)
    num_cols = len(full[0])
    data = make_2d_array(num_rows, num_cols)
    for row, line in enumerate(full):
        for col, char in enumerate(line):
            data[row][col] = int(char)
    full_2d = data

    return sample_2d, full_2d


def get_column(data, col_idx):
    # No way to extract a column without numpy so Just Deal.
    return [row[col_idx] for row in data]


def get_data_lines(problem_number):
    # Return a tuple of (sample data, full data)
    # Based on the problem number. Normal
    # pattern is to have line-specific parsers that operate on the return from this.
    sample_file = f'./data/{problem_number}s.txt'
    data_file = f'./data/{problem_number}.txt'

    sample_data = clean_lines(open(f'./data/{problem_number}s.txt', 'r').readlines())
    full_data = clean_lines(open(f'./data/{problem_number}.txt', 'r').readlines())
    return (sample_data, full_data)


def draw_coordinate_line_closed(tuple_from, tuple_to):
    """Return a list of integer points between two tuples, including the endpoints.

    At the time of this writing, this does not support diagonals: only one dimension
    of endpoint coordinates is allowed to differ between from and to.

    """
    assert len(tuple_from) == len(tuple_to)

    list_delta = []
    for x in range(len(tuple_from)):
        value_from = tuple_from[x]
        value_to   = tuple_to[x]
        assert isinstance(value_from, int)
        assert isinstance(value_to,   int)

        list_delta.append(value_to - value_from)

    count_nonzero_dimensions = len([x for x in list_delta if x != 0])
    assert count_nonzero_dimensions < 2

    raise Exception("This was never finished.  Next time!")

