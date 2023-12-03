from utils import log, load_2d_arrays

# Make a set of known symbols
KNOWN_SYMBOLS = set("+*#$/%&@!?-=<>")

if __name__ == '__main__':
    sample_data, full_data = load_2d_arrays(3)
    for tag, dataset, expected_answer in [
        ("sample", sample_data, 7),
        ("full", full_data, 336),
    ]:
        for row in dataset:
            for character in row:
                if character == '.': continue
                is_integer = False
                # First, is character an integer?
                try:
                    int(character)
                    is_integer = True
                except ValueError:
                    pass
                if is_integer: continue

                if character not in KNOWN_SYMBOLS:
                    raise ValueError(f"Unknown symbol: {character}")
        log.info(f"{tag=} {expected_answer=}")
