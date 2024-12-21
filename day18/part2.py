from __future__ import annotations

import argparse
import heapq
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dijkstra(
    bytes: set[tuple[int, ...]],
    start: tuple[int, int],
    end: tuple[int, int],
    coords: set[tuple[int, int]],
) -> float:
    q = [(0, start)]
    distances = {pos: float('inf') for pos in coords}
    distances[start] = 0

    seen = set()
    while q:
        distance, pos = heapq.heappop(q)
        if pos in seen:
            continue
        seen.add(pos)

        for adj in support.adjacent_4(*pos):
            if adj in coords and adj not in bytes:
                curr_distance = distance + 1

                if curr_distance < distances[adj]:
                    distances[adj] = curr_distance
                    heapq.heappush(q, (curr_distance, adj))

    return distances[end]


def compute(s: str, dim: int, n_bytes: int | None) -> tuple[int, ...]:
    lines = s.splitlines()[:n_bytes] if n_bytes is not None else s.splitlines()
    start, end = (0, 0), (dim, dim)
    bx, by = support.bounds((start, end))

    coords = {(x, y) for y in by.range for x in bx.range}

    bytes = set()
    for line in lines:
        byte_coords = tuple(map(int, line.split(',')))
        bytes.add(byte_coords)
        distance = dijkstra(bytes, start, end, coords)
        if distance == float('inf'):
            return byte_coords

    raise ValueError


INPUT_S = '''\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''
EXPECTED = 6, 1


@pytest.mark.parametrize(
    ('input_s', 'dim', 'n_bytes', 'expected'),
    (
        (INPUT_S, 6, None, EXPECTED),
    ),
)
def test(input_s: str, dim: int, expected: int, n_bytes: int) -> None:
    assert compute(input_s, dim, n_bytes) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 70, None))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
