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
            coords[((x, y))] = c
    return coords


def compute(s: str) -> int:
    coords = parse_coords(s)
    start_pos = [k for k, v in coords.items() if v == '^'][0]
    start_dir = support.Direction4.UP
    total = 0

    for test_pos in coords:
        if coords[test_pos] != '#' and test_pos != start_pos:
            # try an obstacle in this position in a new copy
            coords_try = coords.copy()
            coords_try[test_pos] = 'O'

            # reset start state
            visited = set()
            pos = start_pos
            dir = start_dir

            while True:
                if (pos, dir) in visited:
                    total += 1
                    break
                else:
                    visited.add((pos, dir))
                next_pos = dir.apply(*pos)
                if next_pos not in coords_try:
                    break
                elif coords_try[next_pos] in ('#', 'O'):
                    dir = dir.cw
                else:
                    pos = next_pos
    return total


INPUT_S = '''\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''
EXPECTED = 6


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
