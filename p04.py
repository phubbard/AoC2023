from utils import get_data_lines


def winning_numbers(line: str) -> list:
    # Given a line of input, return a list of the winning numbers
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

    two_lists = line.split(' | ')
    card1_sl = two_lists[0].split(':')[1].strip().split(' ')
    card2_sl = two_lists[1].split(' ')


    c1_filtered = list(filter(lambda x: len(x.strip()) > 0, card1_sl))
    c2_filtered = list(filter(lambda x: len(x.strip()) > 0, card2_sl))

    card1 = [int(x) for x in c1_filtered]
    card2 = [int(x) for x in c2_filtered]

    c1s = set(card1)
    c2s = set(card2)

    a = list(c1s.intersection(c2s))
    return a


def score_game(score_len) -> int:
    if score_len == 0:
        return 0
    return pow(2, score_len  - 1)


def score_data(data: list):
    scores = [len(winning_numbers(x)) for x in data]

    total = sum([score_game(x) for x in scores])
    print(f"Total: {total}")

    return total



if __name__ == '__main__':
    sample, full = get_data_lines(4)
    score_data(sample)
    score_data(full)
