from __future__ import annotations

import argparse
import itertools
import os.path

import numpy as np
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
        # locations where antennas appear
        locs = [pos for pos, c in coords.items() if c == char]

        # 3+ antennas will always be in line with 2 others
        if len(locs) > 2:
            for loc in locs:
                antinodes.add(loc)

        for a, b in itertools.product(locs, locs):
            if a != b:
                np_a, np_b = np.array(a), np.array(b)
                diff = np_b - np_a
                # move backwards until off grid
                cand_back = tuple((np_a - diff).tolist())
                while cand_back in coords:
                    antinodes.add(cand_back)
                    cand_back = tuple((np.array(cand_back) - diff).tolist())

                # move forwards until off grid
                cand_forward = tuple((np_b + diff).tolist())
                while cand_forward in coords:
                    antinodes.add(cand_forward)
                    cand_forward = tuple(
                        (np.array(cand_forward) + diff).tolist(),
                    )
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
EXPECTED = 34


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
