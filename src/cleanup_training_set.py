#!/usr/bin/env python3

import argparse
import html
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


def calc_threshold(src_input, tgt_input):
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

    with open(cmdline.inputpref + '.src') as src_input, \
            open(cmdline.inputpref + '.tgt') as tgt_input:
        src_max_length, tgt_max_length, mean, stddev = \
            calc_threshold(src_input, tgt_input)
    ratio_min = mean - 3 * stddev
    ratio_max = mean + 3 * stddev
    print(f"src_max_length={src_max_length}")
    print(f"tgt_max_length={tgt_max_length}")
    print(f"mean={mean}")
    print(f"stddev={stddev}")
    print(f"ratio_min={ratio_min}")
    print(f"ratio_max={ratio_max}")

    skipped = 0
    unique = set()
    with open(cmdline.inputpref + '.src') as src_input, \
            open(cmdline.inputpref + '.tgt') as tgt_input, \
            open(cmdline.outputpref + '.src', 'w') as src_output, \
            open(cmdline.outputpref + '.tgt', 'w') as tgt_output:
        for src_line, tgt_line in zip(src_input, tgt_input):
            src_length = len(src_line)
            tgt_length = len(tgt_line)
            ratio = src_length / tgt_length
            if src_length > src_max_length or tgt_length > tgt_max_length \
                    or ratio > ratio_max or ratio < ratio_min \
                    or src_length < 5 or tgt_length < 5:
                skipped += 1
                continue
            src_line = html.unescape(src_line.rstrip())
            tgt_line = html.unescape(tgt_line.rstrip())
            key = src_line + '\t' + tgt_line
            if key in unique:
                skipped += 1
                continue
            unique.add(key)
            src_output.write(src_line + '\n')
            tgt_output.write(tgt_line + '\n')
    print(f"skipped {skipped}")


if __name__ == '__main__':
    main()
