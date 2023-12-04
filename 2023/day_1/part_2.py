#!/usr/bin/env python3
"""
--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are 
actually spelled out with letters: one, two, three, four, five, six, seven, 
eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and 
last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

import sys

strs_to_digits: dict[str, str] = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

num_strs = strs_to_digits.keys()


def lmost_num(line: str) -> str:
    for start_idx in range(len(line)):
        if line[start_idx].isdigit():
            return line[start_idx]
        for num_str in num_strs:
            if line[start_idx : start_idx + len(num_str)].startswith(num_str):
                return strs_to_digits[num_str]


def rmost_num(line: str) -> str:
    for end_idx in range(len(line) - 1, -1, -1):
        if line[end_idx].isdigit():
            return line[end_idx]
        for num_str in num_strs:
            if line[end_idx - len(num_str) + 1 : end_idx + 1].endswith(num_str):
                return strs_to_digits[num_str]


def pair(line: str) -> tuple[str, str]:
    return lmost_num(line), rmost_num(line)


def main():
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <filename>', file=sys.stderr)
        exit(1)

    total = 0

    with open(sys.argv[1], 'r') as f:
        for line in f:
            l, r = pair(line)
            print(l, r, sep='', end=' | ')
            print(line, end='')
            total += int(l + r)

    print(total)


if __name__ == '__main__':
    main()
