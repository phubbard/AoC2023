from dataclasses import dataclass
from utils import get_data_lines


@dataclass
class Game:
    number: int = 0
    my_numbers: list = None
    winning_numbers: list = None
    matching_numbers: list = None


def parse_game(line: str) -> Game:
    # Given a game line, return a Game object
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    rc = Game()

    two_lists = line.split(' | ')

    sublist = two_lists[0].split(':')

    filtered_p1 = list(filter(lambda x: len(x.strip()) > 0, sublist[0].strip().split(' ')))
    rc.number = int(filtered_p1[-1])

    card1_sl = sublist[1].strip().split(' ')
    card2_sl = two_lists[1].split(' ')

    c1_filtered = list(filter(lambda x: len(x.strip()) > 0, card1_sl))
    c2_filtered = list(filter(lambda x: len(x.strip()) > 0, card2_sl))

    card1 = [int(x) for x in c1_filtered]
    card2 = [int(x) for x in c2_filtered]

    rc.winning_numbers = card1
    rc.my_numbers = card2
    rc.matching_numbers = list(set(card1).intersection(set(card2)))
    return rc


def winning_numbers(line: str) -> list:
    # Given a line of input, return a list of the winning numbers
    game = parse_game(line)
    return game.matching_numbers


def score_game(score_len) -> int:
    if score_len == 0:
        return 0
    return pow(2, score_len - 1)


def score_data(data: list):
    scores = [len(winning_numbers(x)) for x in data]

    total = sum([score_game(x) for x in scores])
    print(f"Total: {total}")

    return total


def part_two(game) -> int:
    # TODO
    return 30


if __name__ == '__main__':
    sample, full = get_data_lines(4)
    assert score_data(sample) == 13
    assert score_data(full) == 26443
    assert part_two(sample) == 30