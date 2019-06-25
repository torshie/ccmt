#!/usr/bin/env python3


import argparse
import math


def parse_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument('--inputpref', required=True)
    p.add_argument('--outputpref', required=True)
    return p.parse_args()


def calc_length_threshold(lengths):
    s = sorted(lengths, reverse=True)
    offset = int(len(s) * 0.05)
    return s[offset]


def calc_ratio_theshold(ratios):
    s = sum(ratios)
    mean = s / len(ratios)

    total = sum([(x - mean) ** 2 for x in ratios])
    stddev = math.sqrt(total / (len(ratios) - 1))
    return mean, stddev


def calc_theshold(src_input, tgt_input):
    src_length = []
    tgt_length = []
    ratio = []
    for src_line, tgt_line in zip(src_input, tgt_input):
        src_length.append(len(src_line))
        tgt_length.append(len(tgt_line))
        ratio.append(src_length[-1] / tgt_length[-1])

    return (calc_length_threshold(src_length),
        calc_length_threshold(tgt_length), *calc_ratio_theshold(ratio))


def main():
    cmdline = parse_cmdline()

    with open(cmdline.inputpref + '.src', 'rb') as src_input, \
            open(cmdline.inputref + '.tgt', 'rb') as tgt_input:
        pass

    with open(cmdline.inputpref + '.src', 'rb') as src_input, \
            open(cmdline.inputpref + '.tgt', 'rb') as tgt_input, \
            open(cmdline.outputpref + '.src', 'wb') as src_output, \
            open(cmdline.outputpref + '.tgt', 'wb') as tgt_output:
        pass


if __name__ == '__main__':
    main()
