from __future__ import annotations

import argparse
import heapq
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_cheats(
    coords: dict[tuple[int, int], str],
    tracks: list[tuple[int, int]],
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    cheats = set()
    for pos in tracks:
        for d1, d2 in itertools.product(support.Direction4, repeat=2):
            if d1 is not d2.opposite:  # don't undo movement
                one = d1.apply(*pos)
                two = d2.apply(*one)

                if one in tracks and two in tracks:
                    # no sense cheating thru tracks
                    continue

                if one in coords and two in tracks:
                    cheats.add((pos, two))

    return cheats


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

    cheats = get_cheats(coords, tracks)
    distances_from_start = shortest_distances(start, end, tracks)
    base_time = distances_from_start[end]

    distances_to_end = {
        k: base_time - v
        for k, v in distances_from_start.items()
    }

    for cheat_start, cheat_end in cheats:
        savings.append(
            base_time - (
                distances_from_start[cheat_start] + 2
                + distances_to_end[cheat_end]
            ),
        )

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
