from utils import get_data_lines, log


SCORE_5_OF_A_KIND = 7
SCORE_4_OF_A_KIND = 6
SCORE_FULL_HOUSE  = 5
SCORE_3_OF_A_KIND = 4
SCORE_2_PAIR      = 3
SCORE_1_PAIR      = 2
SCORE_HIGH_CARD   = 1


class Hand:
    def __init__(self, cards):
        raw_histogram = {}
        for card in cards:
            value = raw_histogram.get(card, 0)
            raw_histogram[card] = value + 1
        sorted_histogram = sorted(raw_histogram.items(), key=lambda x: x[1], reverse=True)

        self.H_CARDS     = cards
        log.info(f"{self.H_CARDS=} has sorted histogram {sorted_histogram=}")

    def __repr__(self):
        return f"Hand {self.H_CARDS=}"
    
    def __str__(self): return repr(self)


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(7)
    for dataset, expected_p1_answer, expected_p2_answer in [
        (sample_data,      -1,      -1),
        (full_data,        -1,      -1),
    ]:
        for row in dataset:
            hand_cards, bid = row.split()
            hand = Hand(hand_cards)
            log.info(f"{hand=} {bid=}")

        found_p1_answer = 1
        log.info(f"{expected_p1_answer=} {found_p1_answer=}")
        assert expected_p1_answer == found_p1_answer

    log.info(f"Success")
