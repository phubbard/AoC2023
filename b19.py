from utils import get_data_lines, log

import time

class Generator:
    def __init__(self, rows, filename):
        self.__workflows = {}
        self.__partargs  = []

        for row in rows:
            if len(row) == 0: continue
            if row.startswith('{'):
                parameters = row[1:-1]
                self.__partargs.append(row[1:-1])
            else:
                workflow_name, procedure = row.split('{')
                steps = []
                for step_text in procedure.removesuffix('}').split(','):
                    if ':' in step_text:
                        condition, next = step_text.split(':')
                    else:
                        condition, next = None, step_text
                    steps.append((condition, next))
                self.__workflows[workflow_name] = steps
        
        lines = []
        lines +=                [f'parts = [']
        for partarg in self.__partargs:
            lines +=            [f'    Part({partarg}),']
        lines +=                [f']']
        lines +=                [f'']
        for name, steps in self.__workflows.items():
            lines +=            [f'def op_{name}(part):']
            lines +=            [f'    log.info(f"wf.name={name} part.x=" + str(part.x))']
            for condition, next in steps:
                if condition is None:
                    lines +=    [f'    return op_{next}(part)']
                else:
                    lines +=    [f'    if part.{condition}: return op_{next}(part)']
            lines +=            [f'']

        with open(filename, 'w') as f:
            f.write('\n'.join(lines))

    def get_workflow_count(self):
        return len(self.__workflows)

class Part:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self):
        return f"[x={self.x},m={self.m},a={self.a},s={self.s}]"

_accumulator = 0

def op_ZERO(): 
    global _accumulator
    _accumulator = 0


def op_A(part):
    global _accumulator
    partsum = part.x + part.m + part.a + part.s
    _accumulator += partsum
    log.info(f'{part.x=} accepted {partsum}')
    return None


def op_R(part):
    # log.info(f"  REJECTING {part}")
    return None


def op_FINAL():
    global _accumulator
    return _accumulator


if __name__ == '__main__':

    sample_data, full_data = get_data_lines('19')

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                # ("b19_sample.py", sample_data,     19114,               -1),
                ("b19_full.py",     full_data,    432434,               -1),
            ]:
        
        generator = Generator(dataset, tag)

        if expected_p1_answer > -1:
            arrangement_count = 0
            for row in dataset:
                log.info(f"Considering -> {row}")

            with open(tag, 'r') as file:
                script_contents = file.read()
                exec(script_contents)

            op_ZERO()
            for part in parts:
                # log.info(f"Evaluating {part}")
                op_in(part)
            log.info(f'workflows{generator.get_workflow_count()} {len(parts)=}')
            found_p1_answer = op_FINAL()
            log.info(f"Steps: {found_p1_answer=} with {expected_p1_answer=}")
            assert found_p1_answer == expected_p1_answer
        else:
            log.info(f"Skipping part one")

        if expected_p2_answer > -1:
            prev_time = time.time()
            arrangement_count = 0
            for row in dataset:
                log.info(f"For row -> {row=}")
                curr_time = time.time()

                log.info(f"{curr_time - prev_time}:  found {permutations} permutations for {row}")
                prev_time = curr_time
            found_p2_answer = arrangement_count

            log.info(f"Steps: {found_p2_answer=} with {expected_p2_answer=}")
            assert found_p2_answer == expected_p2_answer
        else:
            log.info(f"Skipping part two")

