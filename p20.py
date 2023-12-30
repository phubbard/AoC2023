from utils import get_data_lines, log


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
        # TODO for the inputs, we need a list of dictionaries - name and last value
        self.last = 0
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

    def process(self, input: int):
        # TODO
        pass


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

    def process(self, input: int):
        if input == 1:
            return
        if self.value == 0:
            self.value = 1
            outp_val = 1
        else:
            self.value = 0
            outp_val = 0

        for out in self.outputs:
            log.debug(f'{self.name} -> {out}')
            # TODO object lookup
            out.process(outp_val)


class Default:
    # there are untyped modules eg output that we need to handle.
    def __init__(self, dataline: str):
        self.raw = dataline
        self.name = dataline
        self.outputs = []

    def process(self, input: int):
        log.debug(f'{self.name} {input=}')


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

    def process(self, input: int):
        for out in self.outputs:
            log.debug(f'{self.name} -> {out}')
            # TODO object lookup
            out.process(input)


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


if __name__ == '__main__':
    log.setLevel('DEBUG')
    sample, full = get_data_lines(20)
    log.debug(sample)
    parse_datafile(sample)

