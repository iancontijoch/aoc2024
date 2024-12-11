from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

START, TARGET = 0, 9


def parse_coords(s: str) -> dict[tuple[int, int], int]:
    return {
        (x, y): int(c)
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line)
    }


def compute(s: str) -> int:
    coords = parse_coords(s)
    total = 0
    trailheads = (pos for pos, c in coords.items() if c == START)

    for start in trailheads:
        q = [(start, [start])]
        while q:
            pos, path = q.pop()
            if coords[pos] == TARGET:
                total += 1
            for adj in support.adjacent_4(*pos):
                if adj not in path:
                    if adj in coords and coords[adj] - coords[pos] == 1:
                        q.append((adj, path + [adj]))
    return total


INPUT_S = '''\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''
EXPECTED = 81


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
