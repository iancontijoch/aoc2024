from __future__ import annotations

import argparse
import os.path

import pytest
from collections import deque

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
BLINKS = 25


def blink(numeric_lst: list[str]) -> list[str]:
    numbers, lst = deque(numeric_lst), []
    while numbers:
        c = numbers.popleft()
        if c == '0':
            lst.append('1')
        elif (digit_len := len(c)) % 2 == 0:
            lst.extend([
                c[:digit_len // 2], 
                str(int(c[digit_len // 2 :]))
            ])
        else:
            lst.append(str(int(c) * 2024))
    return lst


def compute(s: str) -> int:
    numeric_lst, lst = [c for c in s.split()], []
    for _ in range(BLINKS):
        if not lst:
            lst = blink(numeric_lst)
        else:
            lst = blink(lst)
    return len(lst)

INPUT_S = '''\
125 17
'''
EXPECTED = 55312


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
