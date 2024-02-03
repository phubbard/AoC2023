from utils import (log, load_2d_arrays,
                   manhattan_distance, get_data_lines,
                   get_column, make_2d_array)


def lines_to_2d(lines):
    arr = []
    for line in lines:
        arr.append(line.split(' '))
    return arr


def data_to_array(data):
    # Dirty hack - sum the moves, create square array that size
    col = get_column(data, 1)
    size = sum([int(x) for x in col])
    log.debug(f'{size=} for new array to draw in'
    return make_2d_array(size, size)


def dig_holes(big_map, input_data):
    # Given a map and a list of instructions, dig holes in the map.
    # The map is a 2D array of integers.
    # The instructions are a list of strings.
    # Each string is a direction and a number of steps.
    # The map is a square
    # The map is a grid of integers.
    position = (0, 0)
    for line in input_data:
        big_map[position[0]][position[1]] = 1
        for _ in len(int(line[1])):
            



if __name__ == '__main__':
    sample, full = get_data_lines(18)
    data = lines_to_2d(sample)
    array = data_to_array(data)
    print(f'{len(array)=}')

