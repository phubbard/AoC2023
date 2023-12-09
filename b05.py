from utils import get_data_lines, log
import time

class Transformer:

    def __init__(self, comment):
        self.TRANSFORMER_COMMENT = comment
        self.TRANSFORMER_TAG     = comment.split('-to-')[1].split()[0]
        self.__range_map = []

    def add_range(self, destination_start, source_start, count):
        self.__range_map.append((destination_start, source_start, count))

    def transform(self, source):
        for destination_start, source_start, count in self.__range_map:
            if source_start <= source < source_start+count:
                return destination_start + (source - source_start)
        return source

if __name__ == '__main__':
    sample_data, full_data = get_data_lines(5)
    for dataset, expected_p1_answer, expected_p2_answer in [
                (sample_data,        35,      46),
                (full_data,   174137457,      -1),
            ]:
        transformers = []
        current_transformer = None
        for row in dataset:
            if 'seeds' in row:
                seeds = tuple(int(x) for x in row.split(':')[1].split())
            elif 'map' in row:
                current_transformer = Transformer(row)
                transformers.append(current_transformer)
            elif len(row_split := row.split()) == 3:
                destination_start, source_start, count = (int(x) for x in row_split)
                current_transformer.add_range(destination_start, source_start, count)
            elif len (row) == 0:
                pass
            else:
                raise Exception(f"Unknown row: {row}")

        def _calculate_one_seed(element):
            annotation = f"Seed {element}, "
            for transformer in transformers:
                element = transformer.transform(element)
                annotation = f"{annotation}{transformer.TRANSFORMER_TAG} {element}, "
            # log.info(f"{annotation}")
            return element, annotation

        log.info(f"Calculating minimum for part one interpretation of seeds")
        minimum_final = None
        for element in seeds:
            value, annotation = _calculate_one_seed(element)
            if minimum_final is None or value < minimum_final:
                minimum_final = value
        log.info(f"{minimum_final=}")
        found_p1_answer = minimum_final
        log.info(f"{expected_p1_answer=} {found_p1_answer=}")
        assert found_p1_answer == expected_p1_answer

        log.info(f"Calculating minimum for part two interpretation of seeds")

        total_runs = 0
        for x in range(0, len(seeds) // 2):
            total_runs += seeds[x*2+1]

        log.info(f"This will need to run {total_runs} times")

        runs_so_far = 0
        minimum_final = None
        for x in range(0, len(seeds) // 2):
            seed  = seeds[x*2]
            count = seeds[x*2+1]
            log.info(f"Seed {seed} count {count} yields...")
            for increment in range(0, count):
                runs_so_far += 1
                if runs_so_far % 1000000 == 0:
                    timestamp_seconds = time.time()
                    log.info(f"{timestamp_seconds=}: Runs so far {runs_so_far}")                
                value, annotation = _calculate_one_seed(seed + increment)
                if minimum_final is None or value < minimum_final:
                    log.info(f"New minimum {value} found at {seed} count {count} with annotation {annotation}")
                    minimum_final = value
        found_p2_answer = minimum_final
        log.info(f"{expected_p2_answer=} {found_p2_answer=}")
        assert found_p2_answer == expected_p2_answer

    log.info(f"Success")


        
