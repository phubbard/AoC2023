from utils import get_data_lines, log

# Queue is a list of tuples (src, dest, value)
# eg ('a', 'b', 1) means a sent 1 to b
work_queue = []

def binary_to_printstr(inp: int) -> str:
    if inp == 0:
        return 'low'
    else:
        return 'high'


class BaseClass:
    def __init__(self, dataline: str):
        self.raw = dataline
        self.name = None
        self.counters = [0, 0]   # low, high
        self.done = False
        self.inputs = {}

    def get_counts(self) -> tuple:
        # low, high
        return self.counters[0], self.counters[1]

    def _parse(self):
        pass

    def add_input(self, name: str):
        self.inputs[name] = 0

    def get_inputs(self) -> list:
        return self.inputs

    def get_outputs(self) -> list:
        if hasattr(self, 'outputs'):
            return self.outputs
        return []

    def send(self, dest: str, value: int):
        self.counters[value] += 1
        work_queue.append((self.name, dest, value))
        log.debug(f'{self.name} -{binary_to_printstr(value)}--> {dest}')

    def process(self, input: int, src_name: str = None):
        pass


# Conjunction modules (prefix &) remember the type of the most recent pulse
# received from each of their connected input modules; they initially default
# to remembering a low pulse for each input. When a pulse is received, the
# conjunction module first updates its memory for that input. Then, if it
# remembers high pulses for all inputs, it sends a low pulse; otherwise, it
# sends a high pulse.
class Conjunction(BaseClass):
    def __init__(self, dataline: str):
        super().__init__(dataline)
        self.outputs = []
        # For the inputs, we need a dictionary - name and last value
        self.inputs = {}
        self._parse()

    def _parse(self):
        # &inv -> a
        tokens = self.raw.split(' -> ')
        assert (len(tokens) == 2)
        self.name = tokens[0][1:]
        destinations = tokens[1].split(',')
        for dest in destinations:
            self.outputs.append(dest.strip())
        log.debug(f'parsed Conjunction: {self.name} -> {self.outputs}')

    def process(self, input: int, src_name: str = None):
        assert (src_name is not None)
        self.inputs[src_name] = input
        if all(self.inputs.values()):
            log.debug(f'{self.name} conj all ones {self.inputs=} flipping to zero -> {self.outputs}')
            outp_val = 0
        else:
            outp_val = 1
        for out in self.outputs:
            self.send(out, outp_val)


# Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high
# pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on
# and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
class FlipFlop(BaseClass):
    def __init__(self, dataline: str):
        super().__init__(dataline)
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

        log.debug(f'parsed FlipFlop: {self.name} -> {self.outputs}')

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
            self.send(out, outp_val)


class Default(BaseClass):
    # there are untyped modules eg output that we need to handle.
    def __init__(self, dataline: str):
        super().__init__(dataline)
        self.name = dataline

    def process(self, input: int, src_name: str = None):
        log.debug(f'{self.name} got {input=} from {src_name}')
        if self.name == 'rx':
            if input == 0:
                self.done = True
                log.info('RX DONE')


class Button(BaseClass):
    def __init__(self, dataline: str):
        super().__init__(dataline)
        self.name = 'button'
        self.outputs = ['broadcaster']

    def go(self):
        self.send('broadcaster', 0)


# There is a single broadcast module (named broadcaster). When it receives a
# pulse, it sends the same pulse to all of its destination modules.
class Broadcaster(BaseClass):
    def __init__(self, dataline: str):
        super().__init__(dataline)
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
        log.debug(f'parsed Broadcaster: {self.name} -> {self.outputs}')

    def process(self, input: int, src_name: str = None):
        for out in self.outputs:
            self.send(out, input)


def process_work_queue(modules, name):
    while len(work_queue) > 0:
        # Queue is a list of tuples (src, dest, value)
        item = work_queue.pop(0)
        modules[item[1]].process(item[2], item[0])


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
        for output in modules[module].get_outputs():
            if output not in modules:
                log.debug(f'Found implied default module: {output}')
                modules[output] = Default(output)

    log.debug('Modules processed, adding Button')
    modules['button'] = Button('button')

    log.debug('Modules processed, scanning for inputs')
    for module in modules:
        for output in modules[module].get_outputs():
            modules[output].add_input(module)

    for module in modules:
        log.debug(f'FINAL {module} in {modules[module].get_inputs()}-> {modules[module].get_outputs()}')

    # TODO generate a graph of nodes and edges - use networkx
    return modules


def dump_counters(modules):
    low_counter = 0
    high_counter = 0

    for module in modules:
        low, high = modules[module].get_counts()
        low_counter += low
        high_counter += high
        log.debug(f'{module} {modules[module].get_counts()=}')
    log.info(f'CNT {low_counter} {high_counter}')


def total_score(modules) -> int:
    low_counter = 0
    high_counter = 0
    for module in modules:
        low, high = modules[module].get_counts()
        low_counter += low
        high_counter += high
    assert low_counter > 0
    assert high_counter > 0
    log.info(f"{low_counter} * {high_counter} = {low_counter * high_counter}")
    return low_counter * high_counter


def run_simulation(modules, name, warmup_count = 1000):
    log.info(f'Running {warmup_count=} warmup cycles')
    for _ in range(warmup_count):
        modules['button'].go()
        process_work_queue(modules, name)

    dump_counters(modules)
    score = total_score(modules)
    log.info(f'{score=} for {name} after {warmup_count} runs')
    if name == 'sample':
        log.warning(f'{score - 11687500} should be 0')


def done(modules):
    return modules['rx'].done


def part_two(modules):
    # Now we keep track of rx and button presses
    button_presses = 0
    while not done(modules):
        modules['button'].go()
        button_presses += 1
        process_work_queue(modules, 'full')

        if button_presses % 100000 == 0:
            log.info(f'RX not done after {button_presses} button presses')

    log.info(f'RX done after {button_presses} button presses')


if __name__ == '__main__':
    log.setLevel('INFO')
    sample, full = get_data_lines(20)
    log.debug(sample)
    run_simulation(parse_datafile(sample), 'sample', warmup_count=1000)

    run_simulation(parse_datafile(full), 'full', warmup_count=1000)

    # part_two(parse_datafile(full))
