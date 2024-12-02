from __future__ import annotations

import argparse
import os.path

import pytest
import math

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def is_safe(lst) -> bool:
    return (
        all(((a < b) and (b - a  in range(1, 4))) 
            for a, b in zip(lst, lst[1:])
        ) or all((a > b) and (a - b in range(1, 4)) 
                 for a, b in zip(lst, lst[1:]))
    )

def is_fixable(lst) -> bool:
    if is_safe(lst):
        return True
    else:
        for i in range(len(lst)):
            if is_safe(lst[:i] + lst[i+1:]):
                return True
    return False

def compute(s: str) -> int:
    safe = 0
    lines = s.splitlines()
    for line in lines:
        report = list(map(int, line.split()))
        safe += is_fixable(report)
    return safe


INPUT_S = '''\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''
EXPECTED = 4


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