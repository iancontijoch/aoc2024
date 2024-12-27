from __future__ import annotations

import argparse
import itertools
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
MOD_NUM = 16777216


def price(n: int) -> int:
    n = n ^ (n << 6) & (MOD_NUM - 1)
    n = ((n >> 5) ^ n) & (MOD_NUM - 1)
    n = ((n << 11) ^ n) & (MOD_NUM - 1)
    return n


def compute(s: str) -> int:
    numbers = support.parse_numbers_split(s)
    seen: dict[tuple[int, ...], int] = defaultdict(int)

    for n in numbers:
        seen_by_buyer = set()
        secret_num = n % 10
        diffs = []
        for i in range(2000):
            tmp = n % 10
            n = price(n)
            diff = (n % 10) - tmp
            diffs.append(diff)
        for i in range(0, len(diffs) - 4):
            delta_batch = tuple(diffs[i:i+4])
            if delta_batch not in seen_by_buyer:
                seen[delta_batch] += (
                    secret_num + sum(itertools.islice(diffs, 0, i+4, None))
                )
                seen_by_buyer.add(delta_batch)
    return max(seen.values())


INPUT_S = '''\
1
2
3
2024
'''
EXPECTED = 23


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
