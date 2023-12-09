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

    def refract(self, *monoranges):
        """Given a set of monoranges, return new monoranges after passing through
        the transformer, including the direct pass through logic."""
        rv = []
        for monorange in monoranges:
            for destination_start, source_start, count in self.__range_map:
                if monorange.MR_START < source_start:
                    # This monorange is entirely before the start of the range
                    # of this transformer.  Just pass it through.
                    rv.append(monorange)
                elif monorange.MR_START < source_start + count:
                    # This monorange starts within the range of this transformer.
                    # It may end within the range of this transformer, or it may
                    # extend beyond the range of this transformer.
                    if monorange.MR_TERMINAL <= source_start + count:
                        # This monorange ends within the range of this transformer.
                        # Pass it through.
                        rv.append(monorange)
                    else:
                        # This monorange extends beyond the range of this transformer.
                        # Split it into two monoranges, one that ends at the end of
                        # the range of this transformer, and one that starts at the
                        # end of the range of this transformer.
                        rv.append(Monorange(monorange.MR_START, source_start + count - monorange.MR_START))
                        rv.append(Monorange(source_start + count, monorange.MR_TERMINAL - (source_start + count)))
                else:
                    # This monorange is entirely after the end of the range of this
                    # transformer.  Just pass it through.
                    rv.append(monorange)
        return rv

class Monorange:

    def __init__(self, start, count):
        self.MR_START    = start
        self.MR_COUNT    = count
        self.MR_TERMINAL = start + count

    def __repr__(self):
        return f"Monorange({self.MR_START}, {self.MR_COUNT})"
    
    def __str__(self):
        return f"Monorange({self.MR_START}, {self.MR_COUNT})"


if __name__ == '__main__':
    sample_data, full_data = get_data_lines(5)
    for dataset, expected_p1_answer, expected_p2_answer in [
                (sample_data,        35,      46),
                # (full_data,   174137457,      -1),
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
        monoranges = []
        for x in range(0, len(seeds) // 2):
            seed  = seeds[x*2]
            count = seeds[x*2+1]
            monoranges.append(Monorange(seed, count))
        for transformer in transformers:
            log.info(f"Sending {len(monoranges)} through transformer {transformer.TRANSFORMER_TAG}...")
            monoranges = transformer.refract(*monoranges)
        log.info(f"finally {len(monoranges)=}")

        found_p2_answer = min(monorange.MR_START for monorange in monoranges)
        log.info(f"{expected_p2_answer=} {found_p2_answer=}")
        assert found_p2_answer == expected_p2_answer

    log.info(f"Success")


        
