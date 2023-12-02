from utils import get_data_as_lines, log

sample_constraint = {'red': 12, 'green': 13, 'blue': 14}
full_constraint = {'red': 12, 'green': 13, 'blue': 14}


def game_max(game: str) -> dict:
    # Given a game line, return a dict with max values for each color
    # EG 'red: 2, green: 3, blue: 4'
    outermost = game.split(':')
    game_num_str = outermost[0].split(' ')[1]
    game_number = int(game_num_str)
    iterations = outermost[1].split(';')
    maxes = {'red': 0, 'green': 0, 'blue': 0, 'game': game_number}
    for iteration in iterations:
        color_strings = iteration.split(',')
        for cs in color_strings:
            # '4 blue '
            cc_str = cs.strip()
            vals = cc_str.split(' ')
            count = int(vals[0])
            color = vals[1].strip()
            if count > maxes[color]:
                maxes[color] = count
    return maxes


def p2_score(maxes: dict) -> int:
    # Given a set of maxes, return the score for part two
    return maxes['red'] * maxes['green'] * maxes['blue']


def is_possible(constraint: dict, maxes: dict) -> bool:
    # Given a constraint and a set of maxes, return True if the constraint is possible
    # EG {'red': 12, 'green': 13, 'blue': 14} {'red': 2, 'green': 3, 'blue': 4}
    for color in constraint:
        if constraint[color] < maxes[color]:
            return False
    return True


if __name__ == '__main__':
    sample = get_data_as_lines(2, 's')
    full = get_data_as_lines(2)

    score = 0
    for line in sample:
        log.debug(f"{game_max(line)=}")
        gm = game_max(line)
        if is_possible(sample_constraint, gm):
            score += gm['game']
    log.info(f"sample {score=}")
    assert score == 8
    full_score = 0
    for line in full:
        log.debug(f"{game_max(line)=}")
        gm = game_max(line)
        if is_possible(full_constraint, gm):
            full_score += gm['game']
    log.info(f"full {full_score=}")

    # part two
    ptwo_score = 0
    for line in sample:
        gm = game_max(line)
        ptwo_score += p2_score(gm)
    log.info(ptwo_score)
    assert ptwo_score == 2286

    score = 0
    for line in full:
        gm = game_max(line)
        score += p2_score(gm)
    log.info(f'full part two {score=}')