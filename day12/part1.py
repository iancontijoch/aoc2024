from __future__ import annotations

import argparse
import itertools
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_coords(s: str) -> dict[tuple[int, int], str]:
    return {
        (x, y): c
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line)
    }


def perimeter(coords: set[tuple[int, int]]) -> int:
    if len(coords) == 1:
        return 4
    offset = sum(
        pos2 in support.adjacent_4(*pos1)
        for pos1, pos2 in itertools.product(coords, repeat=2)
    )

    return 4 * len(coords) - offset


def make_regions(
    coords: dict[tuple[int, int], str],
) -> dict[tuple[str, tuple[int, int]], set[tuple[int, int]]]:
    seen = set()
    regions = defaultdict(set)

    for pos in coords:
        if pos not in seen:
            path = {pos}
            seen.add(pos)

            regions[(coords[pos], pos)] = {pos}
            q = [pos]
            while q:
                cur = q.pop()
                for cand in support.adjacent_4(*cur):
                    if (
                        cand in coords
                        and coords[cand] == coords[cur]
                        and cand not in path
                    ):
                        regions[(coords[pos], pos)].add(cand)
                        seen.add(cand)
                        path.add(cand)
                        q.append(cand)
    return regions


def compute(s: str) -> int:
    coords = parse_coords(s)
    return sum(len(v) * perimeter(v) for _, v in make_regions(coords).items())


INPUT_S = '''\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''
EXPECTED = 1930


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
