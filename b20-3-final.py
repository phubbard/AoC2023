
import csv
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

    for tag, dataset, expected_p1_answer, expected_p2_answer in [
                ("sample", sample_data,       8,      -1),
                ("real",   real_data,      7097,     355),
            ]:
        log(f"Considering -> {tag}")

        found_answer_p1 = 0
        log(f"expected_p1_answer={expected_p1_answer} and found_answer_p1={found_answer_p1}")
        if expected_p1_answer > -1:
            assert found_answer_p1 == expected_p1_answer
        else:
            log(f"Skipping part one")


    log(f"Success")

