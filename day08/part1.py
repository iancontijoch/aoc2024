from __future__ import annotations

import argparse
import itertools
import os.path
from operator import add
from operator import sub

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_coords(s: str) -> dict[tuple[int, int], str]:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
    return coords


def compute(s: str) -> int:
    antenna_chars = tuple({c for c in s if c not in ('.', '\n')})
    antinodes = set()
    coords = parse_coords(s)

    for char in antenna_chars:
        locs = [pos for pos, c in coords.items() if c == char]
        for a, b in itertools.product(locs, locs):
            if a != b:
                diff = tuple(map(sub, b, a))
                anti1, anti2 = (
                    tuple(map(sub, a, diff)),
                    tuple(map(add, b, diff)),
                )
                if anti1 in coords:
                    antinodes.add(anti1)
                if anti2 in coords:
                    antinodes.add(anti2)

    return len(antinodes)


INPUT_S = '''\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''
EXPECTED = 14


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


(4, 3)
(5, 5)
(-1, -2)

(3, 1)
