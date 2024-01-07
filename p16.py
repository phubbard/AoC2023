from utils import load_2d_arrays, log, make_2d_array


work_queue = []
energized_map = [[]]


def next_row_col(row, col, direction):
    nrc = {'R': lambda row, col: (row, col + 1),
           'D': lambda row, col: (row + 1, col),
           'L': lambda row, col: (row, col - 1),
           'U': lambda row, col: (row - 1, col)}
    return nrc[direction](row, col)


def process_step(map: list, row: int, col: int, direction: str):
    mirror_backslash = {'R': 'D', 'D': 'R', 'L': 'U', 'U': 'L'}
    mirror_slash = {'R': 'U', 'D': 'L', 'L': 'D', 'U': 'R'}

    if row < 0 or col < 0 or row >= len(map) or col >= len(map[0]):
        log.debug(f"Out of bounds: {row}, {col}")
        return

    cell = map[row][col]
    energized_map[row][col] = 1
    match cell:
        case '.':
            # Empty space - no-op
            new_row, new_col = next_row_col(row, col, direction)
            work_queue.append((new_row, new_col, direction))
        case '\\':
            new_direction = mirror_backslash[direction]
            new_row, new_col = next_row_col(row, col, new_direction)
            work_queue.append((new_row, new_col, new_direction))
        case '/':
            new_direction = mirror_slash[direction]
            new_row, new_col = next_row_col(row, col, new_direction)
            work_queue.append((new_row, new_col, new_direction))
        case '|':
            if direction in ['U', 'D']:
                # Passthrough
                new_row, new_col = next_row_col(row, col, direction)
                work_queue.append((new_row, new_col, direction))
            else:
                # Split
                new_row, new_col = next_row_col(row, col, 'U')
                work_queue.append((new_row, new_col, 'U'))
                new_row, new_col = next_row_col(row, col, 'D')
                work_queue.append((new_row, new_col, 'D'))
        case '-':
            if direction in ['L', 'R']:
                # Passthrough
                new_row, new_col = next_row_col(row, col, direction)
                work_queue.append((new_row, new_col, direction))
            else:
                # Split
                new_row, new_col = next_row_col(row, col, 'L')
                work_queue.append((new_row, new_col, 'L'))
                new_row, new_col = next_row_col(row, col, 'R')
                work_queue.append((new_row, new_col, 'R'))


def part_one(map, en_map):
    global work_queue
    previous_work = {}
    work_queue.append((0, 0, 'R'))
    while len(work_queue) > 0:
        row, col, direction = work_queue.pop(0)
        if (row, col, direction) in previous_work:
            continue
        previous_work[(row, col, direction)] = True
        process_step(map, row, col, direction)

        # log.debug(f'After step: {row}, {col}, {direction} {map[row][col]} we have {work_queue=}')
    for row in en_map:
        new_row = []
        for entry in row:
            new_row.append('.' if entry == 0 else '#')
        log.debug(''.join(new_row))

    en_count = sum([sum(row) for row in en_map])
    log.info(f"Part one: {en_count}")


if __name__ == '__main__':
    log.setLevel('DEBUG')
    sample, full = load_2d_arrays(16)
    energized_map = make_2d_array(len(sample), len(sample[0]))
    part_one(sample, energized_map)

    energized_map = make_2d_array(len(full), len(full[0]))
    part_one(full, energized_map)