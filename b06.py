from utils import get_data_lines, log


class RaceSpec:
    def __init__(self, time, distance):
        self.RS_TIME     = time
        self.RS_DISTANCE = distance

    def __repr__(self):
        return f"RaceSpec {self.RS_TIME=} {self.RS_DISTANCE=}"


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(6)
    for dataset, expected_p1_answer, expected_p2_answer in [
                    (sample_data,        -1,      -1),
                    (full_data,          -1,      -1),
                ]:
        time_array = None
        distance_array = None
        for row in dataset:
            if 'Time' in row:
                if time_array is not None: raise Exception("Multiple time arrays")
                time_array = [int(x) for x in dataset[0].split(':')[1].split()]
            elif 'Distance' in row:
                if distance_array is not None: raise Exception("Multiple distance arrays")
                distance_array = [int(x) for x in dataset[1].split(':')[1].split()]
            else: raise Exception(f"Unknown row: {row}")
        assert len(time_array) == len(distance_array), \
            "Time and distance arrays must be the same length"
        
        # Now we have two integer arrays to process
        for time, distance in zip(time_array, distance_array):
            raceSpec = RaceSpec(time, distance)
            log.info(f"Considering {raceSpec=} ...")
        
        found_p1_answer = 0
        log.info(f"{expected_p1_answer=} {found_p1_answer=}")
        assert expected_p1_answer == found_p1_answer

    log.info(f"Success")

