from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

SECONDS = 100


def print_coords(
    coords: set[tuple[int, int]],
    width: int,
    length: int,
) -> None:
    print(
        '\n'.join(
            ''.join([f'{str.zfill(f'{y}', 3)}: '] + [
                '#' if (x, y)
                in coords else '.' for x in range(width)
            ])
            for y in range(length)
        ),
    )


def compute(s: str, width: int, length: int) -> int:
    lines = s.splitlines()
    seconds = 0
    while True:
        locations: dict[tuple[int, int], int] = defaultdict(int)
        for line in lines:
            p, v = line.split()
            px, py = tuple(map(int, p.split('=')[1].split(',')))
            vx, vy = tuple(map(int, v.split('=')[1].split(',')))

            px, py = (px + seconds * vx) % width, (py + seconds * vy) % length
            locations[(px, py)] += 1

        clusters = [
            pos for pos in locations if all(
                adj in locations for adj in support.adjacent_8(*pos)
            )
        ]
        if clusters:
            # print_coords(locations, width, length)
            return seconds

        seconds += 1


INPUT_S = '''\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''
EXPECTED = 12


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 11, 7) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 101, 103))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
