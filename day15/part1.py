from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_coords(s: str) -> dict[tuple[int, int], str]:
    return {
        (x, y): c
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line)
    }


def move(
    d: support.Direction4,
    pos: tuple[int, int],
    coords: dict[tuple[int, int], str],
) -> dict[tuple[int, int], str]:

    cand = d.apply(*pos)
    if pos in coords and cand in coords:
        if coords[cand] == '#':
            return coords
        if coords[cand] == '.':
            coords[cand] = coords[pos]
            coords[pos] = '.'
            if coords[cand] == 'O':  # retroactively apply moves
                coords = move(d, d.opposite.apply(*pos), coords)
            return coords
        if coords[cand] == 'O':
            coords = move(d, cand, coords)
    return coords


def compute(s: str) -> int:
    dmap = {
        '^': support.Direction4.UP,
        '>': support.Direction4.RIGHT,
        'v': support.Direction4.DOWN,
        '<': support.Direction4.LEFT,
    }

    coords_s, moves_s = s.split('\n\n')
    coords = parse_coords(coords_s)
    moves = (
        dmap.get(c) for c
        in moves_s.replace('\n', '')
    )
    pos = [k for k, v in coords.items() if v == '@'][0]
    for m in moves:
        if m is not None:
            pos = [k for k, v in coords.items() if v == '@'][0]
            coords = move(m, pos, coords)

    return sum(100 * y + x for x, y in coords if coords[(x, y)] == 'O')


INPUT_S = '''\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''
EXPECTED = 10092


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
