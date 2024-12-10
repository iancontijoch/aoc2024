from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def has_gap(lst: list[str]) -> bool:
    last_num_ix = 0
    for i, c in enumerate(reversed(lst)):
        if c != '.':
            last_num_ix = len(lst) - 1 - i
            break
    return last_num_ix > lst.index('.')


def swap(lst: list[str]) -> list[str]:
    right_pointer = -1
    while right_pointer >= -len(lst):
        c = lst[right_pointer]
        if c.isnumeric() and '.' in lst:
            idx_space = lst.index('.')
            lst[idx_space] = c
            lst[right_pointer] = '.'
        right_pointer -= 1
    # fix first element
    if lst[0] == '.':
        lst = lst[1:] + ['.']

    return lst


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        numbers = list(map(int, line))
        files = ([str(i)] * n for i, n in enumerate(numbers[::2]))
        free_space = (['.'] * n for n in numbers[1::2])
        block_lst = [
            c for c in
            itertools.chain(
                *itertools.zip_longest(files, free_space),
            )
            if c is not None
        ]

        flattened_lst = [x for y in block_lst for x in y]
        swapped = swap(flattened_lst)
        total += sum(
            i * int(c)
            for i, c in enumerate(swapped[:swapped.index('.')])
        )

    return total


INPUT_S = '''\
2333133121414131402
'''
EXPECTED = 1928


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
