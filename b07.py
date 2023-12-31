from utils import get_data_lines, log
from functools import cmp_to_key

SCORE_5_OF_A_KIND = 6
SCORE_4_OF_A_KIND = 5
SCORE_FULL_HOUSE  = 4
SCORE_3_OF_A_KIND = 3
SCORE_2_PAIR      = 2
SCORE_1_PAIR      = 1
SCORE_HIGH_CARD   = 0

TIEBREAK = 'AKQJT987654321'

class Hand:
    def __init__(self, cards, bid):
        raw_histogram = {}
        for card in cards:
            value = raw_histogram.get(card, 0)
            raw_histogram[card] = value + 1
        sorted_histogram = sorted(raw_histogram.items(), key=lambda x: x[1], reverse=True)
        first_card, first_count   = sorted_histogram[0]
        second_card, second_count = sorted_histogram[1] if len(sorted_histogram) > 1 else (None, 0)

        if first_count == 5:
            category = SCORE_5_OF_A_KIND
        elif first_count == 4:
            category = SCORE_4_OF_A_KIND
        elif first_count == 3:
            if second_count == 2:
                category = SCORE_FULL_HOUSE
            else:
                category = SCORE_3_OF_A_KIND
        elif first_count == 2:
            if second_count == 2:
                category = SCORE_2_PAIR
            else:
                category = SCORE_1_PAIR
        else:
            category = SCORE_HIGH_CARD

        self.H_CARDS      = cards
        self.H_CATEGORY   = category
        self.H_BID        = bid

    def __repr__(self):
        return f"Hand {self.H_CARDS=} with {self.H_CATEGORY=} and {self.H_BID=}"
    
    def __str__(self): return repr(self)


def compare_hand_strength(hand1, hand2):
    for card1, card2 in zip(hand1.H_CARDS, hand2.H_CARDS):
        if card1 == card2: continue
        return TIEBREAK.index(card1) - TIEBREAK.index(card2) 
    return 0


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(7)
    for dataset, expected_p1_answer, expected_p2_answer in [
        (sample_data,      6440,      -1),
        (full_data,   255048101,      -1),
    ]:
        raw_hands = []
        for row in dataset:
            hand_cards, bid = row.split()
            hand = Hand(hand_cards, int(bid))
            log.info(f"{hand=} {bid=}")
            raw_hands.append(hand)

        # Rank the hands, first by 
        strength_sorted_hands = sorted(raw_hands, key=cmp_to_key(compare_hand_strength), reverse=True)
        full_sorted_hands     = sorted(strength_sorted_hands, key=lambda x: x.H_CATEGORY, reverse=False)
        for hand in strength_sorted_hands: log.info(f"strengthsort: {hand=}")
        for hand in full_sorted_hands:     log.info(f"fullsort: {hand=}")

        winnings = 0
        for index, hand in enumerate(full_sorted_hands):
            winnings += hand.H_BID * (index + 1)

        found_p1_answer = winnings
        log.info(f"{expected_p1_answer=} {found_p1_answer=}")
        assert expected_p1_answer == found_p1_answer

    log.info(f"Success")
