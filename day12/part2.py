from __future__ import annotations

import argparse
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


def get_corners(
    points: set[tuple[int, int]],
) -> set[tuple[tuple[int, int], str]]:
    corners = set()
    for point in points:
        if support.Direction4.LEFT.apply(*point) not in points:
            if support.Direction4.UP.apply(*point) not in points:
                # top-left corner (F):
                corners.add((point, 'F'))
            if support.Direction4.DOWN.apply(*point) not in points:
                # bottom-left corner (L):
                corners.add((point, 'L'))
        if support.Direction4.RIGHT.apply(*point) not in points:
            if support.Direction4.UP.apply(*point) not in points:
                # top-right corner (7):
                corners.add((point, '7'))
            if support.Direction4.DOWN.apply(*point) not in points:
                # bottom-right corner (J):
                corners.add((point, 'J'))
        if support.Direction4.UP.apply(*point) in points:
            if (
                support.Direction4.RIGHT.apply(*point) in points and
                support.Direction8.NE.apply(*point) not in points
            ):
                corners.add((point, '7'))
            if (
                support.Direction4.LEFT.apply(*point) in points and
                support.Direction8.NW.apply(*point) not in points
            ):
                corners.add((point, 'F'))
        if support.Direction4.DOWN.apply(*point) in points:
            if (
                support.Direction4.RIGHT.apply(*point) in points and
                support.Direction8.SE.apply(*point) not in points
            ):
                corners.add((point, 'J'))
            if (
                support.Direction4.LEFT.apply(*point) in points and
                support.Direction8.SW.apply(*point) not in points
            ):
                corners.add((point, 'L'))
    return corners


def compute(s: str) -> int:
    coords = parse_coords(s)
    regions = make_regions(coords)

    return sum(len(v) * len(get_corners(v)) for _, v in regions.items())


INPUT_S = '''\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
'''
EXPECTED = 368


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
