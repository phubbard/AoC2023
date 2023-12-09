from utils import get_data_lines, log




def compare_eqr_hands(a: str, b: str) -> str:
    # Compare two hands of equal rank
    # Return ">" if a wins, "<" if b wins, "=" if tie
    card_strength = "AKQJT98765432"
    log.info(f"Comparing {a=} {b=}")
    cur_idx = 0
    while cur_idx < len(a) - 1:
        a_card = a[cur_idx]
        b_card = b[cur_idx]
        a_str = card_strength.index(a_card)
        b_str = card_strength.index(b_card)
        if a_str < b_str:
            return ">"
        if b_str < a_str:
            return "<"
        cur_idx += 1
    return "="


def compare_hands(a: str, b: str) -> str:
    a_rank = rank_hand(a)
    b_rank = rank_hand(b)
    if a_rank == b_rank:
        return compare_eqr_hands(a, b)
    if rank_hand(a) > rank_hand(b):
        return ">"
    return "<"


def rank_hand(cards: str) -> int:
    # 1 (high card) to 7 (five of a kind)
    card_counts = {}
    for card in cards:
        card_counts[card] = card_counts.get(card, 0) + 1

    c_set = set(cards)
    # 5 of a kind
    if len(c_set) == 1:
        return 7
    # 4 of a kind or full house
    if len(c_set) == 2:
        if 2 in card_counts.values():
            return 5
        else:
            return 6
    # 3 of a kind or two pair
    if len(c_set) == 3:
        if 2 in card_counts.values():
            return 3
        else:
            return 4
    # One pair
    if len(c_set) == 4:
        return 2
    # High card
    return 1


test_data = {
    'AAAAA': 7,
    'AA8AA': 6,
    '23332': 5,
    'TTT98': 4,
    '23432': 3,
    'A23A4': 2,
    '23456': 1,
}


def validate_scoring():
    for hand, expected_rank in test_data.items():
        assert rank_hand(hand) == expected_rank, f"Failed {hand=} {expected_rank=} {rank_hand(hand)=}"
    log.info(f"Success")


test_hands = [
    {'a': '33332', 'b': '2AAAA', 'expected': '>'},
    {'a': '77888', 'b': '77788', 'expected': '>'},
    {'a': '22222', 'b': '22222', 'expected': '='},
]


def validate_hand_comparisons():
    for hand in test_hands:
        assert compare_hands(hand['a'], hand['b']) == hand['expected'], f"Failed {hand=} {compare_hands(hand['a'], hand['b'])=}"


if __name__ == '__main__':
    validate_scoring()
    validate_hand_comparisons()

    sample, full = get_data_lines(7)
    winnings = 0
    for line in sample:
        cards, bid = line.split()
        winnings += (int(bid) * rank_hand(cards))
    log.info(f"sample {winnings=}")
