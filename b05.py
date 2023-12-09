from utils import get_data_lines, log


class Transformer:

    def __init__(self, comment):
        self.TRANSFORMER_COMMENT = comment
        self.TRANSFORMER_TAG     = comment.split('-to-')[1].split()[0]
        self.__range_map = []

    def add_range(self, destination_start, source_start, count):
        self.__range_map.append((destination_start, source_start, count))

    def concretize(self):
        remapped = {}
        for destination_start, source_start, count in self.__range_map:
            for i in range(count):
                remapped[source_start + i] =  destination_start + i
        self.__mapping = remapped
        del self.__range_map

    def transform(self, source):
        return self.__mapping.get(source, source)
    

if __name__ == '__main__':
    sample_data, full_data = get_data_lines(5)
    for dataset, expected_p1_answer, expected_p2_answer in [
                (sample_data,    -1,      -1),
                (full_data,      -1,      -1),
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
        [x.concretize() for x in transformers]
        for seed in seeds:
            annotation = f"Seed {seed}, "
            for transformer in transformers:
                seed = transformer.transform(seed)
                annotation = f"{annotation}{transformer.TRANSFORMER_TAG} {seed}, "
            log.info(f"{annotation}")


        found_p1_answer = 1
        found_p2_answer = 1

        log.info(f"{expected_p1_answer=} {found_p1_answer=}")
        assert found_p1_answer == expected_p1_answer
        log.info(f"{expected_p2_answer=} {found_p2_answer=}")
        assert found_p2_answer == expected_p2_answer

    log.info(f"Success")


        
