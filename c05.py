from utils import get_data_lines, log
import time


class Transformer:

    def __init__(self, comment):
        self.TRANSFORMER_COMMENT = comment
        self.TRANSFORMER_TAG     = comment.split('-to-')[1].split()[0]
        self.range_map = []

    def add_range(self, destination_start, source_start, count):
        self.range_map.append((destination_start, source_start, count))

    def transform(self, source):
        for destination_start, source_start, count in self.range_map:
            if source_start <= source < source_start+count:
                return destination_start + (source - source_start)
        return source

    #Had to add this because, well math.  Basically to get the break points for
    #seeds you have to invert intermediat breakpoints back to seeds domain.
    def inverse_transform(self,source):
        for destination_start, source_start, count in self.range_map:
            if destination_start <= source < destination_start+count:
                return source_start + (source - destination_start)
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

        log.info(f"Calculating minimum for part two interpretation of seeds\n")

        #Getting a superset of the breakpoints for the composite of all of the transforms
        da_breaks = []
        for t_ind in range(len(transformers)):
            t = transformers[t_ind]
            t_breaks = [r[0] for r in t.range_map]
            t_breaks.extend([r[0] + r[2] for r in t.range_map])  #This line is to catch a very small potential bug
            t_breaks.sort()
            t_breaks = list(set(t_breaks))

            for b_ind in range(t_ind,-1,-1):
                tr = transformers[b_ind]
                t_breaks = [tr.inverse_transform(x) for x in t_breaks]
            log.info(f"Transformer {t_ind} adds {t_breaks}")
            da_breaks.extend(t_breaks)

        da_breaks.sort()
        da_breaks = list(set(da_breaks))
        log.info(f"{da_breaks=}")
        # assert 82 in da_breaks

        total_runs = 0
        for x in range(0, len(seeds) // 2):
            total_runs += seeds[x * 2 + 1]

        total_runs =(len(da_breaks) + 1)*len(seeds)//2
        log.info(f"This will need to run {total_runs} times")

        runs_so_far = 0
        minimum_final = None

        for xxx in range(0, len(seeds) // 2):
            seed  = seeds[xxx * 2]
            count = seeds[xxx * 2 + 1]

            #Only testing the parts of da_breaks that are in range of the seed
            test = [x for x in da_breaks if x >= seed and x < seed + count]
            test.append(seed)
            log.info(f"Seed {seed} count {len(test)} yields...")
            log.info(f"minimum_final {minimum_final}")
            #for increment in range(0, count):
            for tseed in test:
                runs_so_far += 1
                if runs_so_far % 100 == 0:
                    timestamp_seconds = time.time()
                    log.info(f"{timestamp_seconds=}: Runs so far {runs_so_far}")                
                value, annotation = _calculate_one_seed(tseed )
                if minimum_final is None or value < minimum_final:
                    log.info(f"New minimum {value} found at {tseed} count {count} with annotation {annotation}")
                    minimum_final = value
        found_p2_answer = minimum_final
        log.info(f"{expected_p2_answer=} {found_p2_answer=}")
        # assert found_p2_answer == expected_p2_answer

    log.info(f"Success")


        
