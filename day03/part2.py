from __future__ import annotations

import argparse
import os.path
import re
import math

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    enabled = True
    for line in lines:
        dos = [(m.span()[0], 'do') 
               for m in re.finditer(r'do\(\)', line)]
        donts = [(m.span()[0], 'dont') 
                 for m in re.finditer(r'don\'t\(\)', line)]
        mults = [(m.span()[0], 'mult', math.prod(map(int, m.groups()))) 
                 for m in re.finditer(r'mul\((\d+),(\d+)\)', line)]
        
        markers = sorted(dos + donts + mults)
        for m in markers:
            if m[1] == 'dont':
                enabled = False
            if m[1] == 'do':
                enabled = True
            if m[1] == 'mult':
                total += enabled * m[2]
                
    return total


INPUT_S = '''\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''
EXPECTED = 48


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())