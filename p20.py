from utils import get_data_lines, log

# Queue is a list of tuples (src, dest, value)
# eg ('a', 'b', 1) means a sent 1 to b
work_queue = []


class Counter():
    def __init__(self, name: str):
        self.name = name
        self.low_counter = 0
        self.high_counter = 0

    def count(self, value: int):
        if value == 0:
            self.low_counter += 1
        else:
            self.high_counter += 1
        log.debug(f'{self.name} {self.low_counter=} {self.high_counter=}')

    def score(self):
        self.total_score = self.low_counter * self.high_counter
        log.debug(f'{self.name} {self.low_counter=} {self.high_counter=} {self.total_score=}')
        return self.total_score

# Conjunction modules (prefix &) remember the type of the most recent pulse
# received from each of their connected input modules; they initially default
# to remembering a low pulse for each input. When a pulse is received, the
# conjunction module first updates its memory for that input. Then, if it
# remembers high pulses for all inputs, it sends a low pulse; otherwise, it
# sends a high pulse.
class Conjunction:
    def __init__(self, dataline: str):
        self.raw = dataline
        self.name = None
        self.outputs = []
        self.inputs = {}
        # For the inputs, we need a dictionary - name and last value
        self._parse()

    def _parse(self):
        # &inv -> a
        tokens = self.raw.split(' -> ')
        assert (len(tokens) == 2)
        self.name = tokens[0][1:]
        destinations = tokens[1].split(',')
        for dest in destinations:
            self.outputs.append(dest.strip())
        log.debug(f'Conjunction: {self.name} -> {self.outputs}')

    def process(self, input: int, src_name: str = None):
        assert (src_name is not None)
        self.inputs[src_name] = input
        if all(self.inputs.values()):
            log.debug(f'{self.name} conj all ones {self.inputs=} flipping to zero -> {self.outputs}')
            outp_val = 0
        else:
            outp_val = 1
        for out in self.outputs:
            log.debug(f'{self.name} {outp_val}-> {out}')
            work_queue.append((self.name, out, outp_val))

# Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high
# pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on
# and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
class FlipFlop:
    def __init__(self, dataline: str):
        self.raw = dataline
        self.name = None
        self.value = 0
        self.outputs = []
        self._parse()

    def _parse(self):
        # %a -> inv, con
        tokens = self.raw.split(' -> ')
        assert (len(tokens) == 2)
        self.name = tokens[0][1:]
        destinations = tokens[1].split(',')
        for dest in destinations:
            self.outputs.append(dest.strip())
        log.debug(f'FlipFlop: {self.name} -> {self.outputs}')

    def process(self, input: int, src_name: str = None):
        if input == 1:
            return
        if self.value == 0:
            self.value = 1
            outp_val = 1
        else:
            self.value = 0
            outp_val = 0

        for out in self.outputs:
            log.debug(f'{self.name} {outp_val}-> {out}')
            work_queue.append((self.name, out, outp_val))


class Default:
    # there are untyped modules eg output that we need to handle.
    def __init__(self, dataline: str):
        self.raw = dataline
        self.name = dataline
        self.outputs = []

    def process(self, input: int, src_name: str = None):
        log.debug(f'{self.name} got {input=} from {src_name}')


# There is a single broadcast module (named broadcaster). When it receives a
# pulse, it sends the same pulse to all of its destination modules.
class Broadcaster:
    def __init__(self, dataline: str):
        self.raw = dataline
        self.name = 'broadcaster'
        self.outputs = []
        self._parse()

    def _parse(self):
        # a -> b, c, d
        tokens = self.raw.split(' -> ')
        assert (len(tokens) == 2)
        assert tokens[0] == 'broadcaster'
        destinations = tokens[1].split(',')
        for dest in destinations:
            self.outputs.append(dest.strip())

        log.debug(f'Broadcaster: {self.name} -> {self.outputs}')

    def process(self, input: int, src_name: str = None):
        for out in self.outputs:
            log.debug(f'{src_name} -> {self.name} {input}-> {out}')
            # send src, dest, value for printf
            work_queue.append((self.name, out, input))


def process_work_queue(modules, name):
    counter = Counter(name)
    while len(work_queue) > 0:
        # Queue is a list of tuples (src, dest, value)
        item = work_queue.pop(0)
        log.debug(f'Processing work queue: {item}')
        counter.count(item[2])
        modules[item[1]].process(item[2], item[0])

    return counter.score()


def parse_datafile(datalines: list):
    modules = {}
    for line in datalines:
        if line.startswith('&'):
            mod = Conjunction(line)
        elif line.startswith('%'):
            mod = FlipFlop(line)
        elif line.startswith('broadcaster'):
            mod = Broadcaster(line)
        else:
            raise Exception(f'Unknown module type: {line}')
        modules[mod.name] = mod

    log.debug('Modules processed, scanning for default modules')
    for module in modules.copy():
        for output in modules[module].outputs:
            if output not in modules:
                log.debug(f'Found implied default module: {output}')
                modules[output] = Default(output)
    for module in modules:
        log.debug(f'{module} -> {modules[module].outputs}')

    return modules


def run_simulation(modules, name, warmup_count = 1000) -> int:
    log.info(f'Running {warmup_count=} warmup cycles')
    score = 0
    for _ in range(warmup_count):
        modules['broadcaster'].process(0)
        score += process_work_queue(modules, name)
    log.info(f'{score=} for {name}')


if __name__ == '__main__':
    log.setLevel('INFO')
    sample, full = get_data_lines(20)
    log.debug(sample)
    parse_datafile(sample)
    run_simulation(parse_datafile(sample), 'sample', warmup_count=1000)

