from utils import get_data_lines, log

card_strength = "AKQJT98765432"


def compare_hands(a: str, b: str) -> str:
    if a == b: return "="
    if rank_hand(a) > rank_hand(b):
        return ">"
    return "<"


def rank_hand(cards: str) -> int:
    # Zero (high card) to 6 (five of a kind)
    card_counts = {}
    for card in cards:
        card_counts[card] = card_counts.get(card, 0) + 1

    # Check for five of a kind
    for card, count in card_counts.items():
        if count == 5:
            return 6
        if count == 4:
            return 5
        if count == 3:
            # final two cards must not be the same as each other or the triple



if __name__ == '__main__':
    sample, full = get_data_lines(6)
    rank_hand('32T3K')
