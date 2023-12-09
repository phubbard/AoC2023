# Mothballing my stumbling into trying to make a too-complex pass fail
# criteria.  I didn't get to an answer before Chris's handmath deduced
# the 'gotcha' of this problem, which was big ints.  I'm going to
# mothball.

from utils import get_data_lines, log

class RaceSpec:
    def __init__(self, time, distance):
        self.RS_TIME     = time
        self.RS_DISTANCE = distance

    def calculate_ways_to_win(self):
        win_count = 0
        distance = 0
        for speed in range(self.RS_TIME):
            run_duration = self.RS_TIME - speed
            distance = run_duration * speed
            # log.info(f"Holding button for {speed=} {run_duration=} {distance=}")
            if distance > self.RS_DISTANCE: win_count += 1
        return win_count

    def __repr__(self):
        return f"RaceSpec {self.RS_TIME=} {self.RS_DISTANCE=}"


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(6)
    for dataset, expected_p1_answer, expected_p2_answer in [
                    (sample_data,       288,      -1),
                    (full_data,     1155175,      -1),
                ]:
        p1_time_array     = None
        p1_distance_array = None
        p2_time_array     = None
        p2_distance_array = None
        for row in dataset:
            if 'Time' in row:
                if p1_time_array is not None: raise Exception("Multiple time arrays")
                p1_time_array = [int(x) for x in dataset[0].split(':')[1].split()]
                p2_time_array = [int(x) for x in dataset[1].split(':')[1].split()]
            elif 'Distance' in row:
                if p1_distance_array is not None: raise Exception("Multiple distance arrays")
                p1_distance_array = [int(x) for x in dataset[1].split(':')[1].split()]
            else: raise Exception(f"Unknown row: {row}")
        assert len(p1_time_array) == len(p1_distance_array), \
            "Time and distance arrays must be the same length"
        
        # Now we have two integer arrays to process
        found_p1_answer = 1
        for time, distance in zip(p1_time_array, p1_distance_array):
            p1_race_spec = RaceSpec(time, distance)
            p1_win_count = p1_race_spec.calculate_ways_to_win()
            found_p1_answer *= p1_win_count
            log.info(f"Considering {p1_race_spec=} with {p1_win_count=} ways to win")
        
        log.info(f"{expected_p1_answer=} {found_p1_answer=}")
        assert expected_p1_answer == found_p1_answer

        found_p2_answer = 1
        p2_race_spec = RaceSpec(prod(p1_time_array), prod(p1_distance_array))
        log.info(f"Considering {p2_race_spec=} ...")

        log.info(f"{expected_p2_answer=} {found_p2_answer=}")
        assert expected_p2_answer == found_p2_answer

    log.info(f"Success")

