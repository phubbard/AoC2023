from utils import get_data_lines, log
import time

class Transformer:

    def __init__(self, comment):
        self.TRANSFORMER_COMMENT = comment
        self.TRANSFORMER_TAG     = comment.split('-to-')[1].split()[0]
        self.__range_map = []

    def add_range(self, destination_start, source_start, count):
        self.__range_map.append((destination_start, source_start, count))
        
    def range_descriptions(self):
        facts = [(ss, ss + c - 1, ds, ds + c - 1) for ds, ss, c in self.__range_map]
        sorted_facts = sorted(facts, key=lambda x: x[0])
        return [f"  {ss}-{se} to {ds}-{de}" for ss, se, ds, de in sorted_facts]  

    def transform(self, source):
        for destination_start, source_start, count in self.__range_map:
            if source_start <= source < source_start+count:
                return destination_start + (source - source_start)
        return source

    def refract(self, monorange):
        """Given a monorange, return a set of monoranges after applying
        the transformer.  Additionally return monoranges for any original
        values not transformed."""
        uncut_monoranges = [monorange]
        log.info(f"Refracting  --> {uncut_monoranges}")
        cut_monoranges = []
        for destination_start, source_start, count in self.__range_map:
            for monorange in uncut_monoranges:
                if monorange.MR_LAST < source_start:
                    log.info("    Whole monorange is before the rangemap segment: no transform")
                    cut_monoranges.append(monorange)
                elif monorange.MR_FIRST >= source_start + count:
                    log.info("    Whole monorange is after the rangemap segment: no transform")
                    cut_monoranges.append(monorange)
                else:
                    log.info("    At least one portion of the monorange must be transformed...")
                    prefix  = None
                    infix   = None
                    postfix = None

                    first = monorange.MR_FIRST
                    last  = monorange.MR_LAST
                    if first < source_start:
                        log.info("    The first part of the monorange is not transformed")
                        prefix = Monorange(first, source_start-1)
                        first = source_start
                    if last >= source_start + count:
                        log.info("    The last part of the monorange is not transformed")
                        postfix = Monorange(source_start+count, last)
                        last = source_start + count - 1
                    log.info("    The middle part of the monorange is transformed")
                    infix = Monorange(destination_start + (first - source_start),
                                      destination_start + (last  - source_start))
                    if prefix:  cut_monoranges.append(prefix)
                    if infix:   cut_monoranges.append(infix)
                    if postfix: cut_monoranges.append(postfix)
            uncut_monoranges = cut_monoranges
            cut_monoranges = []
        log.info(f"  Returning --> {uncut_monoranges}")
        return uncut_monoranges


class Monorange:

    def __init__(self, first, last):
        self.MR_FIRST = first
        self.MR_LAST  = last

    def __repr__(self):
        return f"Monorange({self.MR_FIRST}-{self.MR_LAST})"
    
    def __str__(self):
        return f"Monorange({self.MR_FIRST}-{self.MR_LAST})"


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
            monoranges.append(Monorange(seed, seed + count - 1))
        for transformer in transformers:
            log.info(f"Current monoranges are...")
            for monorange in monoranges:
                log.info(f"    {monorange}")
            log.info(f"Sending {len(monoranges)} through transformer {transformer.TRANSFORMER_TAG} with")
            for description in transformer.range_descriptions():
                log.info(f"    {description}")
            new_monoranges = []
            for monorange in monoranges:
                new_monoranges += transformer.refract(monorange)
            monoranges = new_monoranges
        log.info(f"finally {len(monoranges)=}")

        found_p2_answer = min(monorange.MR_FIRST for monorange in monoranges)
        log.info(f"{expected_p2_answer=} {found_p2_answer=}")
        assert found_p2_answer == expected_p2_answer

    log.info(f"Success")


        
