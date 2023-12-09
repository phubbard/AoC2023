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
                (full_data,   174137457, 1493866),
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

# VERY LONG RUN TRANSCRIPT SNIPPETS:
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(67): INFO This will need to run 2398198298 times
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(74): INFO Seed 1132132257 count 323430997 yields...
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(82): INFO New minimum 2774465761 found at 1132132257 count 323430997 with annotation Seed 1132132257, soil 2060608563, fertilizer 4111587153, water 3317982992, light 3875532737, temperature 3527232275, humidity 2021460085, location 2774465761,
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084467.162698: Runs so far 1000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084480.1291494: Runs so far 2000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084493.16586: Runs so far 3000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084506.2742686: Runs so far 4000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084519.2258282: Runs so far 5000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084532.2494774: Runs so far 6000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084545.2539265: Runs so far 7000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084558.1465757: Runs so far 8000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702084571.0007048: Runs so far 9000000

# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702113684.0281627: Runs so far 2394000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702113698.9208403: Runs so far 2395000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702113713.8153803: Runs so far 2396000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702113728.6360059: Runs so far 2397000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(79): INFO timestamp_seconds=1702113743.5745652: Runs so far 2398000000
# /cygdrive/c/home/bhyslop/phubbard/AoC2023/b05.py(85): INFO expected_p2_answer=-1 found_p2_answer=1493866
        
