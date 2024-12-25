from __future__ import annotations

import argparse
import heapq
import itertools
import os.path
from collections.abc import Generator
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

c2d = {
    '<': support.Direction4.LEFT,
    '>': support.Direction4.RIGHT,
    'v': support.Direction4.DOWN,
    '^': support.Direction4.UP,
}

d2c = {
    support.Direction4.LEFT: '<',
    support.Direction4.RIGHT: '>',
    support.Direction4.UP: '^',
    support.Direction4.DOWN: 'v',
}


def shortest_paths(
    coords: dict[tuple[int, int], str],
    start: tuple[int, int],
    end: tuple[int, int],
) -> list[list[str]]:

    paths = []
    q: list[
        tuple[
            tuple[int, int], int, support.Direction4,
            list[str],
        ]
    ] = [(start, 0, support.Direction4.UP, [])]
    distances = {pos: float('inf') for pos in coords}
    while q:
        pos, distance, direction, path = heapq.heappop(q)
        path += [d2c.get(direction, '')]
        if pos == end:
            if distance < distances[end]:
                distances[end] = distance
            if distance == distances[end]:
                paths.append(path[1:])
            continue
        for dir in support.Direction4:
            adj = dir.apply(*pos)
            if adj in coords:
                if distances[adj] > distance:
                    distances[adj] = distance + 1
                    heapq.heappush(q, (adj, distance + 1, dir, path[:]))
    return paths


def get_possible_paths(
    code: str, keypad: dict[tuple[int, int], str],
    start: tuple[int, int],
) -> tuple[tuple[list[str], ...], ...]:
    pos = start
    paths = []
    for key in code:
        key_coords = next(pos for pos, c in keypad.items() if c == key)
        paths.append(shortest_paths(keypad, pos, key_coords))
        pos = key_coords

    return tuple(itertools.product(*paths))


def flatten(nested_lst: Any) -> Generator[Any]:
    for item in nested_lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def format_possible_paths(
    possible_paths: tuple[tuple[list[str], ...], ...],
) -> list[str]:
    return [
        'A'.join(
            ''.join(sublist)
            for sublist in group
        ) + 'A'
        for group in possible_paths
    ]


def compute(s: str) -> int:
    total = 0
    codes = s.splitlines()
    n_keypad = {
        (0, 0): '7',
        (1, 0): '8',
        (2, 0): '9',
        (0, 1): '4',
        (1, 1): '5',
        (2, 1): '6',
        (0, 2): '1',
        (1, 2): '2',
        (2, 2): '3',
        (1, 3): '0',
        (2, 3): 'A',
    }

    d_keypad1 = {
        (1, 0): '^',
        (2, 0): 'A',
        (0, 1): '<',
        (1, 1): 'v',
        (2, 1): '>',
    }

    d_keypad2 = d_keypad1.copy()
    NUMPAD_START = (2, 3)

    for code in codes:

        paths_kp = format_possible_paths(
            get_possible_paths(code, n_keypad, NUMPAD_START),
        )

        paths_dkp1 = [
            x for x in flatten(
                format_possible_paths(
                    get_possible_paths(path, d_keypad1, (2, 0)),
                )
                for path in paths_kp
            )
        ]

        paths_dkp2 = [
            x for x in flatten(
                format_possible_paths(
                    get_possible_paths(path, d_keypad2, (2, 0)),
                )
                for path in paths_dkp1
            )
        ]

        min_code = min(paths_dkp2, key=lambda x: len(x))
        total += int(code[:-1]) * len(min_code)
    return total


INPUT_S = '''\
029A
980A
179A
456A
379A
'''
EXPECTED = 126384


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
