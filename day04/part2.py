from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_coords(s: str) -> dict[tuple[int, int], str]:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
    return coords


def check_tile_totals(
    x: int, y: int,
    coords: dict[tuple[int, int], str],
) -> bool:

    nw, se = (
        support.Direction8.NW.apply(x, y),
        support.Direction8.SE.apply(x, y),
    )

    sw, ne = (
        support.Direction8.SW.apply(x, y),
        support.Direction8.NE.apply(x, y),
    )

    if all(c in coords for c in (nw, se, sw, ne)):
        return (coords[nw], coords[se], coords[sw], coords[ne]) in (
            ('M', 'S', 'S', 'M'),
            ('M', 'S', 'M', 'S'),
            ('S', 'M', 'S', 'M'),
            ('S', 'M', 'M', 'S'),
        )
    else:
        return False


def compute(s: str) -> int:
    total = 0
    coords = parse_coords(s)
    for coord in coords:
        if coords[coord] == 'A':
            total += check_tile_totals(*coord, coords)
    return total


INPUT_S = '''\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''
EXPECTED = 9


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
