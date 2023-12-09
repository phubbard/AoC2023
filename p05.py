from utils import get_data_lines
from multiprocessing import Pool
from functools import lru_cache
from itertools import batched, starmap

xforms = []


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


# @lru_cache(maxsize=1048596)
def run_xforms(value: int) -> int:
    global xforms
    global_min = 1e9
    for xformer in xforms:
        value = xformer.lookup(value)
        global_min = min(global_min, value)
    return int(global_min)


def worker_fn(seed_min: int, seed_count: int) -> int:
    # Process a range of seeds and return the minimum value found
    global_min = run_xforms(seed_min)
    seed_max = seed_min + seed_count
    for seed in range(seed_min, seed_max):
        global_min = int(min(global_min, run_xforms(seed)))
    print(f"Worker {seed_min},{seed_max} {seed_max - seed_min=} returning {global_min=}")
    return global_min


def parse_inp_lines(data: list):
    global xforms
    current_xformer = None
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

    # part 1
    min_final = None
    for seed in seeds:
        # print(f"Seed {seed}")
        for xformer in xforms:
            seed = xformer.lookup(seed)
            # print(f" - {xformer.name} {seed}")
        if min_final is None or seed < min_final:
            min_final = seed
        # print(f"{min_final=}")

    print(f"part 1 {min_final=}")

    ########################
    print("part 2")
    seed_ranges = list(batched(seeds, 2))

    total_search_count = sum([x[0] + x[1] for x in seed_ranges])
    print(f"{total_search_count=}")
    pool = Pool()

    results = starmap(worker_fn, seed_ranges)
    l_global_min = int(min(results))

    print(f"part 2 {l_global_min=}")


if __name__ == '__main__':
    sample, final = get_data_lines(5)
    parse_inp_lines(sample)
    parse_inp_lines(final)

