from __future__ import annotations

import argparse
import heapq
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_cheat_lengths(
    x: int, y: int, n: int,
    coords: dict[tuple[int, int], str],
    tracks: list[tuple[int, int]],
    d_from_start: dict[tuple[int, int], float],
    d_to_end: dict[tuple[int, int], float],
) -> list[int]:

    cheat_lengths: list[int] = []
    distance_from_start = d_from_start[(x, y)]

    points_by_level = defaultdict(set)
    points_by_level[0].add((x, y))
    seen = set()

    for i in range(n):
        new_points = {
            x for pt in points_by_level[i]
            for x in support.adjacent_4(*pt)
            if x in coords and x not in seen
        }
        seen.update(new_points)

        for point in new_points:
            if point in tracks:
                cheat_lengths.append
                (
                    distance_from_start +
                    (i+1) +
                    d_to_end[point]
                )

        points_by_level[i+1].update(new_points)
    return cheat_lengths


def shortest_distances(
    start: tuple[int, int],
    end: tuple[int, int],
    tracks: list[tuple[int, int]],
) -> dict[tuple[int, int], float]:
    distances = {pos: float('inf') for pos in tracks}

    q = [(start, 0)]
    while q:
        pos, distance = heapq.heappop(q)

        if distance < distances[pos]:
            distances[pos] = distance

        if pos == end:
            break

        for adj in support.adjacent_4(*pos):
            if adj in tracks:
                if distances[adj] > distance + 1:
                    heapq.heappush(q, (adj, distance + 1))

    return distances


def compute(s: str) -> int:
    savings = []

    coords = support.parse_coords(s)
    start = next(pos for pos in coords if coords[pos] == 'S')
    end = next(pos for pos in coords if coords[pos] == 'E')
    tracks = [pos for pos in coords if coords[pos] in 'SE.']

    distances_from_start = shortest_distances(start, end, tracks)
    base_time = distances_from_start[end]

    distances_to_end = {
        k: base_time - v
        for k, v in distances_from_start.items()
    }

    cheats = defaultdict(list)
    for pos in tracks:
        cheats[pos] = get_cheat_lengths(
            *pos,
            20,
            coords,
            tracks,
            distances_from_start,
            distances_to_end,
        )

    for pos_cheats in cheats.values():
        for cheat in pos_cheats:
            if base_time - cheat >= 50:
                savings.append(base_time - cheat)

    return len([s for s in savings if s >= 100])


INPUT_S = '''\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''
EXPECTED = 0


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
