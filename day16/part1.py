from __future__ import annotations

import argparse
import heapq
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dijkstra(
        graph: dict[
            tuple[tuple[int, int], support.Direction4],
            list[
                tuple[
                    tuple[int, int],
                    support.Direction4,
                    int,
                ]
            ],
        ],
        start: tuple[int, int],
        end: tuple[int, int],
) -> float:
    q: list[
        tuple[
            int,
            tuple[int, int],
            support.Direction4,
            list[tuple[int, int]],
        ]
    ] = [
        (0, start, support.Direction4.RIGHT, []),
    ]
    min_cost = float('inf')
    # Dictionary to track the best cost for each (node, direction)
    best_cost: dict[tuple[tuple[int, int], support.Direction4], int] = {}

    while q:
        cost, pos, direction, path = heapq.heappop(q)
        path = path + [pos]

        if cost > min_cost:
            continue

        if ((pos, direction) in best_cost and
                cost > best_cost[(pos, direction)]):
            continue

        best_cost[(pos, direction)] = cost

        if pos == end:
            min_cost = cost
        else:
            for neighbor, d, weight in graph[(pos, direction)]:
                heapq.heappush(q, (cost + weight, neighbor, d, path))

    return min_cost


def compute(s: str) -> int:
    coords = support.parse_coords(s)

    start = next(pos for pos, c in coords.items() if c == 'S')
    end = next(pos for pos, c in coords.items() if c == 'E')
    spaces = [pos for pos, c in coords.items() if c in 'ES.']

    graph = defaultdict(list)
    # build weighted graph
    for pos in spaces:
        for d in support.Direction4:
            for d2 in (d, d.cw, d.ccw):
                if d2.apply(*pos) in spaces:
                    graph[(pos, d)].append(
                        (d2.apply(*pos), d2, 1 if d2 is d else 1001),
                    )

    return int(dijkstra(graph, start, end))


INPUT_S_1 = '''\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''
EXPECTED_1 = 7036

INPUT_S_2 = '''\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''
EXPECTED_2 = 11048


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
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
