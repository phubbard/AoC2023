
class Transform:
    def __init__(self):
        self.name = 'Unknown'
        self.src_ranges = []
        self.dest_ranges = []

    def add_range(self, dest_start: int, src_start: int, count: int):
        self.src_ranges.append((src_start, count))
        self.dest_ranges.append((dest_start, count))

    def lookup(self, src: int) -> int:
        for idx, (start, count) in enumerate(self.src_ranges):
            if src >= start and src < start + count:
                return self.dest_ranges[idx][0] + (src - start)
        raise ValueError(f"Could not find {src} in {self.src_ranges}")

def generate_map(input_lines: list, name: str) -> dict:

    maps = []
    for line in input_lines:
        numbers = [int(x) for x in line.split(' ')]
        assert len(numbers) == 3

        instance = Transform(numbers[1], numbers[0], numbers[2], name)
        maps.append(instance)

    return maps


if __name__ == '__main__':
    tdata = '''50 98 2
52 50 48'''
    tname = 'seed-to-soil'
    tlines = tdata.split('\n')
    tmaps = generate_map(tlines, tname)
    print(tmaps)
