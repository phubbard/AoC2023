
import collections
import inspect
import os


def safe_dictionary_insert(key, value, dictionary):
    if key in dictionary: raise Exception(f"Key {key} already in dictionary")
    dictionary[key] = value
    return value


def log(message):
    frameNudge = 0
    caller = inspect.getframeinfo(inspect.stack(context=1 + frameNudge)[1 + frameNudge][0])
    _, filename = os.path.split(caller.filename)
    print("%s(%d): %s" % (filename, caller.lineno, message))



if __name__ == '__main__':

    sample_data = open("data/20s.txt").read()
    real_data = open("data/20.txt").read()

    for tag, dataset in [
                ("sample", sample_data),
                ("real",   real_data),
            ]:
        log(f"Considering -> {tag}")

        broadcaster = [] # list of destinations
        flip_flops  = collections.defaultdict(list) # Name to list of destinations
        inverters   = collections.defaultdict(list) # Name to list of destinations
        for line in dataset.split('\n'):
            if line.startswith('broadcaster'):
                tokens = line.split(' -> ')
                assert (len(tokens) == 2)
                assert tokens[0] == 'broadcaster'
                destinations = tokens[1].split(',')
                for dest in destinations:
                    broadcaster.append(dest.strip())
            elif line.startswith('%'):
                line = line.replace('%', '')
                token, destinations = line.split(' -> ')
                for dest in destinations.split(','):
                    flip_flops[token].append(dest.strip())
            elif line.startswith('&'):
                line = line.replace('&', '')
                token, destinations = line.split(' -> ')
                for dest in destinations.split(','):
                    inverters[token].append(dest.strip())
            else:
                raise Exception(f"Unknown line: {line}")
        
        broadcaster_label = "BC"

        lines = []
        lines +=             ['digraph finite_state_machine {']
        lines +=             [f'    graph [layout=fdp];']
        lines +=             [f'    fontname="Helvetica,Arial,sans-serif"']
        lines +=             [f'    node [fontname="Helvetica,Arial,sans-serif"]']
        lines +=             [f'    edge [fontname="Helvetica,Arial,sans-serif"]']
        lines +=             [f'    rankdir=LR;']
        lines +=             [f'    node [shape = rectangle]; "{broadcaster_label}";']
        lines +=             [f'    node [shape = triangle]; {" ".join(inverters.keys())};']
        lines +=             [f'    node [shape = square]; {" ".join(flip_flops.keys())};']
        
        for dest in broadcaster:
            lines +=         [f'    "{broadcaster_label}" -> {dest};']    
        for inverter, destinations in inverters.items():
            for d in destinations:
                lines +=     [f'    {inverter} -> {d} ;']
        for flip_flop, destinations in flip_flops.items():
            for d in destinations:
                lines +=     [f'    {flip_flop} -> {d} ;']

        lines +=             ['}']

        # finally, write to file
        with open(f"b20-gv-{tag}.dot", 'w') as file:
            file.write('\n'.join(lines))

    log(f"Success")

