from utils import get_data_lines, log

def score_data(data):
    pass

if __name__ == '__main__':
    sample_data, full_data = get_data_lines(4)
    for dataset, expected_p2_answer in [
                (sample_data,      30),
                (full_data,   6284877),
            ]:
        current_card = 1
        card_win_dict = {}
        for row in dataset:
            card_meta, card_info = row.split(':')
            text_set_a, text_set_b = card_info.split('|')
            set_a = set(int(x) for x in text_set_a.split())
            set_b = set(int(x) for x in text_set_b.split())
            wins = len(set_a.intersection(set_b))
            log.info(f"{current_card=} had {wins=}")
            card_win_dict[current_card] = wins
            current_card += 1
        instance_dict = {c:1 for c in card_win_dict.keys()}
        for card_number, wins in card_win_dict.items():
            card_instance = instance_dict[card_number]
            for win in range(wins):
                adjusted = card_number + win + 1
                instance_dict[adjusted] += card_instance
        for card_number, instances in instance_dict.items():
            log.info(f"{card_number=} had {instances=}")
        total_instances = sum (instance_dict.values())
        log.info(f"{total_instances=}")
        assert total_instances == expected_p2_answer
    log.info(f"Success")


        
