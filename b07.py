from utils import get_data_lines, log


class Hand:
    def __init__(self, cards):
        self.H_CARDS = cards

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
