from utils import get_data_lines, log
from dataclasses import dataclass
import re


@dataclass
class Part:
    x: int = None
    m: int = None
    a: int = None
    s: int = None


class Rule:
    # represents a single rule in a workflow
    # e.g. a<2006:qkq
    def __init__(self, rule_text: str):
        self.rule_text = rule_text
        self.operator = None
        self.variable = None
        self.value = None
        self.dest = None
        self.parse()

    def parse(self):
        # a<2006:qkq
        pattern = r'(\w)([<>])(\d+):(\w+)'
        groups = re.match(pattern, self.rule_text)
        if groups is None:
            return

        self.variable = groups[1]
        self.operator = groups[2]
        self.value = int(groups[3])
        self.dest = groups[4]

    def compare(self, part: Part) -> bool:
        # a<2006
        match self.operator:
            case '<':
                return part.__dict__[self.variable] < self.value
            case '>':
                return part.__dict__[self.variable] > self.value
            case _:
                raise ValueError(f'Unknown operation {self.operator}')

    def evaluate(self, part: Part) -> str:
        if self.compare(part):
            return self.dest
        else:
            return None


@dataclass
class Workflow:
    name: str = None
    rules: list = None
    default_dest: str = None


def parse_workflow(dataline: str) -> Workflow:
    # eg px{a<2006:qkq,m>2090:A,rfg}
    wf = Workflow()
    wf.rules = []
    pattern = r'(\w+){(.+)}'
    groups = re.match(pattern, dataline)

    wf.name = groups[1]

    op_tokens = groups[2].split(',')
    assert op_tokens is not None

    for current in op_tokens:
        rule_tokens = current.split(':')
        if len(rule_tokens) == 1:
            wf.default_dest = current
            continue
        rule = Rule(current)
        wf.rules.append(rule)

    return wf


def evaluate_wf(workflows: dict, wf_name: str, part: Part) -> int:
    # Run the workflow on the part.
    # If accepted, return the sum, otherwise 0
    if wf_name == 'R':
        return 0
    if wf_name == 'A':
        p_total = sum(part.__dict__.values())
        log.debug(f'{part.x=} accepted {p_total}')
        return p_total

    log.debug(f'{wf_name=}')

    wf = workflows[wf_name]
    log.debug(f'{wf.name=} {part.x=}')
    assert wf is not None

    for rule in wf.rules:
        dest = rule.evaluate(part)
        if dest:
            return evaluate_wf(workflows, rule.dest, part)

    return evaluate_wf(workflows, wf.default_dest, part)


def parse_part(dataline: str) -> Part:
    # eg {x=787,m=2655,a=1222,s=2876}
    trimmed = dataline[1:-1]
    tokens = trimmed.split(',')
    part = Part()
    for current in tokens:
        key, value = current.split('=')
        r_val = int(value)
        match key:
            case 'x':
                part.x = r_val
            case 'm':
                part.m = r_val
            case 'a':
                part.a = r_val
            case 's':
                part.s = r_val
            case _:
                raise ValueError(f'Unknown part {key}')

    assert part.x is not None
    assert part.m is not None
    assert part.a is not None
    assert part.s is not None

    # log.info(f'{part=} {dataline=}')
    return part


def parse_data(datalines: list) -> tuple:
    workflows = {}
    parts = []
    for line in datalines:
        if not line:
            continue
        if line.startswith('{'):
            parts.append(parse_part(line))
        else:
            wf = parse_workflow(line)
            workflows[wf.name] = wf
    return workflows, parts


if __name__ == '__main__':
    log.setLevel('INFO')
    log.debug(f'{parse_workflow("px{a<2006:qkq,m>2090:A,rfg}")=}')
    sample, full = get_data_lines('19')
    workflows, parts = parse_data(sample)
    log.info(f'{sum([evaluate_wf(workflows, "in", part) for part in parts])=}')

    workflows, parts = parse_data(full)

    p1_answer = 432434
    f_sum = sum([evaluate_wf(workflows, "in", part) for part in parts])
    log.info(f'{f_sum=}')
    log.debug(f'{len(workflows)=} {len(parts)=}')
