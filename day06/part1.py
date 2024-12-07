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
    pos = [k for k, v in coords.items() if v == '^'][0]
    visited = set()
    dir = support.Direction4.UP

    while True:
        visited.add(pos)
        next_pos = dir.apply(*pos)
        if next_pos not in coords:
            break
        elif coords[next_pos] == '#':
            dir = dir.cw
        else:
            pos = next_pos
    return len(visited)


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
EXPECTED = 41


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
