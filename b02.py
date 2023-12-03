from utils import get_data_as_lines

sample_constraint = {'red': 12, 'green': 13, 'blue': 14}
full_constraint = {'red': 12, 'green': 13, 'blue': 14}

colors = ('red', 'green', 'blue')

def get_largest(row):
    prefix = 'Game '
    if not row.startswith(prefix): raise Exception("BAD")
    game_split = row.removeprefix(prefix).split(':')
    if len(game_split) != 2: raise Exception("BAD")
    id = int(game_split[0])
    largest_dict = {c:0 for c in colors}
    for round in game_split[1].split(';'):
        for phrase in round.split(','):
            for c in colors:
                if c in phrase:
                    value = int(phrase.split()[0])
                    largest_dict[c] = max(largest_dict[c], value)
    return id, largest_dict

def determine_possibility(rows):
    output_value = 0
    for row in rows:
        id, largest = get_largest(row)
        is_possible = True
        for color in colors:
            is_possible = is_possible and largest[color] <= sample_constraint[color]
        # print(id, largest, is_possible)
        if is_possible:
            output_value += id
    return output_value

def determine_fewest(rows):
    output_value = 0
    for row in rows:
        id, largest = get_largest(row)
        local_product = 1
        for color in colors:
            local_product *= largest[color]
        output_value += local_product
    return output_value

if __name__ == '__main__':
    for name, correct_possibility, correct_fewest, lines in [
            ('sample',    8,  2286, get_data_as_lines(2, 's')),
            ('full',   2348, 76008, get_data_as_lines(2)),
            ]:
        possibility_value = determine_possibility(lines)
        fewest_value      = determine_fewest(lines)
        print(f'{name}: {possibility_value=} {fewest_value=}')
        assert possibility_value == correct_possibility
        assert fewest_value == correct_fewest
    print("SUCCESS")
