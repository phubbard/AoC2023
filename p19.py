from utils import get_data_lines, log
from dataclasses import dataclass
import re


@dataclass
class Part:
    x: int = None
    m: int = None
    a: int = None
    s: int = None

@dataclass
class Workflow:
    name: str = None
    default_dest: str = None
    x_op: str = None
    m_op: str = None
    a_op: str = None
    s_op: str = None
    x_val: int = None
    m_val: int = None
    a_val: int = None
    s_val: int = None
    x_dest: str = None
    m_dest: str = None
    a_dest: str = None
    s_dest: str = None


def parse_workflow(dataline: str) -> Workflow:
    # eg px{a<2006:qkq,m>2090:A,rfg}
    wf = Workflow()
    pattern = r'(\w+){(.+)}'
    groups = re.match(pattern, dataline)
    wf.name = groups[1]
    op_tokens = groups[2].split(',')
    for current in op_tokens:
        rule_tokens = current.split(':')
        if len(rule_tokens) != 2:
            wf.default_dest = current
            continue
        match current[0]:
            case 'a':
                wf.a_op = current[1:2]
                wf.a_val = int(rule_tokens[0][2:])
                wf.a_dest = rule_tokens[1]
            case 'm':
                wf.m_op = current[1:2]
                wf.m_val = int(rule_tokens[0][2:])
                wf.m_dest = rule_tokens[1]
            case 's':
                wf.s_op = current[1:2]
                wf.s_val = int(rule_tokens[0][2:])
                wf.s_dest = rule_tokens[1]
            case 'x':
                wf.x_op = current[1:2]
                wf.x_val = int(rule_tokens[0][2:])
                wf.x_dest = rule_tokens[1]
            case _:
                raise ValueError(f'Unknown operation {current[0]}')

    # TODO save order of operations
    return wf


def parse_part(dataline: str) -> Part:
    # eg {x=787,m=2655,a=1222,s=2876}
    trimmed = dataline[1:-1]
    parts = trimmed.split(',')
    part = Part()
    for current in parts:
        key, value = current.split('=')
        match key:
            case 'x':
                part.x = int(value)
            case 'm':
                part.m = int(value)
            case 'a':
                part.a = int(value)
            case 's':
                part.s = int(value)
            case _:
                raise ValueError(f'Unknown part {key}')
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
    log.setLevel('DEBUG')
    log.debug(f'{parse_workflow("px{a<2006:qkq,m>2090:A,rfg}")=}')
    sample, full = get_data_lines('19')
    workflows, parts = parse_data(sample)
    pass

