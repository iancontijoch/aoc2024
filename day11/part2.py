from __future__ import annotations

import argparse
import functools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@functools.cache
def change(c: str, blinks: int) -> int:
    if blinks == 0:
        return len([c])
    if c == '0':
        return change('1', blinks - 1)
    elif (digit_len := len(c)) % 2 == 0:
        return (
            change(c[:digit_len // 2], blinks - 1) +
            change((str(int(c[digit_len // 2:]))), blinks - 1)
        )
    else:
        return change(str(int(c) * 2024), blinks - 1)


def compute(s: str, blinks: int) -> int:
    return sum(change(c, blinks) for c in s.split())


INPUT_S = '''\
125 17
'''


@pytest.mark.parametrize(
    ('input_s', 'blinks', 'expected'),
    (
        (INPUT_S, 6, 22),
        (INPUT_S, 25, 55312),
    ),
)
def test(input_s: str, blinks: int, expected: int) -> None:
    assert compute(input_s, blinks) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), blinks=75))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
