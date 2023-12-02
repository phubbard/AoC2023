from utils import get_data_as_lines

sample_constraint = {'red': 12, 'green': 13, 'blue': 14}
full_constraint = {'red': 12, 'green': 13, 'blue': 14}

colors = ('red', 'green', 'blue')

def get_largest(row):
    prefix = 'Game '
    if not row.startswith(prefix): raise Exception("BAD")
    gamesplit = row.removeprefix(prefix).split(':')
    if len(gamesplit) != 2: raise Exception("BAD")
    id = int(gamesplit[0])
    largest_dict = {c:0 for c in colors}
    for round in gamesplit[1].split(';'):
        for phrase in round.split(','):
            for c in colors:
                if c in phrase:
                    value = int(phrase.split()[0])
                    largest_dict[c] = max(largest_dict[c], value)
    return id, largest_dict

def determine_sum(rows):
    output_value = 0
    for row in rows:
        id, largest = get_largest(row)
        is_possible = True
        for color in colors:
            is_possible = is_possible and largest[color] <= sample_constraint[color]
        print(id, largest, is_possible)
        if is_possible:
            output_value += id
    return output_value

if __name__ == '__main__':
    for name, lines in {'sample': get_data_as_lines(2, 's'), 'full': get_data_as_lines(2)}.items():
        output_value = determine_sum(lines)
        print(f'{name}: {output_value=}')
 