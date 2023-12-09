from utils import get_data_lines


class Transform:
    def __init__(self, comment: str):
        self.name = comment.split('-to-')[1].split()[0]
        self.src_ranges = []
        self.dest_ranges = []

    def add_range(self, dest_start: int, src_start: int, count: int):
        self.src_ranges.append((src_start, count))
        self.dest_ranges.append((dest_start, count))

    def lookup(self, src: int) -> int:
        for idx, (start, count) in enumerate(self.src_ranges):
            if src >= start and src < start + count:
                return self.dest_ranges[idx][0] + (src - start)

        return src


def parse_inp_lines(data: list):
    xforms = []
    current_xformer = None
    seed_ranges = []
    for line in data:
        if len(line.strip()) == 0:
            continue
        if 'seeds' in line:
            seeds = [int(x) for x in line.split(':')[1].split()]
            
        elif 'map' in line:
            current_xformer = Transform(line)
            xforms.append(current_xformer)
        else:
            numbers = [int(x) for x in line.split(' ')]
            assert len(numbers) == 3
            current_xformer.add_range(numbers[0], numbers[1], numbers[2])

    min_final = None
    for seed in seeds:
        print(f"Seed {seed}")
        for xformer in xforms:
            seed = xformer.lookup(seed)
            print(f"  {xformer.name} {seed}")
        if min_final is None or seed < min_final:
            min_final = seed
        print(f"{min_final=}")

    print(f"{min_final=}")


if __name__ == '__main__':
    sample, final = get_data_lines(5)
    parse_inp_lines(sample)
    parse_inp_lines(final)

