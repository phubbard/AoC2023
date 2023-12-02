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

if __name__ == '__main__':
    sample = get_data_as_lines(2, 's')
    full = get_data_as_lines(2)

    for row in sample:
        print(get_largest(row))
