from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _height(
    coords: dict[tuple[int, int], str],
    reverse: bool = False,
) -> tuple[int, ...]:
    bx, by = support.bounds(coords)
    func = min if reverse else max
    sign = -1 if reverse else 1

    return tuple(
        (reverse * by.max) + sign * func(
            pos[1]
            for pos, c in coords.items()
            if c == '#' and pos[0] == x
        )
        for x in bx.range
    )


def compute(s: str) -> int:
    total = 0
    schematics = s.split('\n\n')
    locks, keys = [], []
    for schematic in schematics:
        coords = support.parse_coords(schematic)
        if {c for pos, c in coords.items() if pos[1] == 0} == set('#'):
            locks.append(coords)
        else:
            keys.append(coords)

    for lock in locks:
        lock_height = [h+1 for h in _height(lock)]
        for key in keys:
            key_height = [h+1 for h in _height(key, reverse=True)]
            if all(a + b < 8 for a, b in zip(lock_height, key_height)):
                total += 1

    return total


INPUT_S = '''\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''
EXPECTED = 3


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
