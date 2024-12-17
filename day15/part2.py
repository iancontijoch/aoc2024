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


def can_move(
    d: support.Direction4,
    pos: tuple[int, int],
    coords: dict[tuple[int, int], str],
) -> bool:

    cand = d.apply(*pos)
    cand_c = coords[cand]
    if cand_c == '.':
        return True
    if cand_c == '#':
        return False

    if cand_c not in '[]':
        raise ValueError

    other_dir = (
        support.Direction4.RIGHT
        if cand_c == '['
        else support.Direction4.LEFT
    )

    if d in (support.Direction4.UP, support.Direction4.DOWN):
        return can_move(d, cand, coords) and can_move(
            d, other_dir.apply(*cand), coords,
        )
    else:
        return can_move(d, cand, coords)


def push(
    d: support.Direction4,
    boxes: set[tuple[int, int]],
    coords: dict[tuple[int, int], str],
) -> dict[tuple[int, int], str]:

    moves = {
        support.Direction4.UP: ((0, -1), lambda x: x[1]),
        support.Direction4.DOWN: ((0, 1), lambda x: -x[1]),
        support.Direction4.LEFT: ((-1, 0), lambda x: x[0]),
        support.Direction4.RIGHT: ((1, 0), lambda x: -x[0]),
    }

    move_offset, sort_key = moves[d]

    for x, y in sorted(boxes, key=sort_key):
        dx, dy = move_offset
        new_pos = (x + dx, y + dy)
        if new_pos not in coords or new_pos == '#':
            return coords
        coords[new_pos] = coords[(x, y)]
        coords[(x, y)] = '.'

    return coords


def find_boxes(
    pos: tuple[int, int],
    d: support.Direction4,
    coords: dict[tuple[int, int], str],
    seen: set[tuple[int, int]] | None = None,
) -> set[tuple[int, int]]:

    pos_c = coords[pos]

    if seen is None:
        seen = {pos}

    if pos_c in '.#':
        return seen

    if d in (support.Direction4.LEFT, support.Direction4.RIGHT):
        adj = d.apply(*pos)
        if adj in coords and coords[adj] in '[]' and adj not in seen:
            seen.add(adj)
            seen = find_boxes(adj, d, coords, seen)
    elif d in (support.Direction4.UP, support.Direction4.DOWN):
        other_dir = (
            support.Direction4.LEFT
            if pos_c == ']'
            else support.Direction4.RIGHT
        )
        other_half = other_dir.apply(*pos)
        next_pos = d.apply(*pos)

        for adj in (other_half, next_pos):
            if adj in coords and coords[adj] in '[]' and adj not in seen:
                seen.add(adj)
                seen = find_boxes(adj, d, coords, seen)
    else:
        raise ValueError

    return seen


def move(
    d: support.Direction4,
    pos: tuple[int, int],
    coords: dict[tuple[int, int], str],
) -> dict[tuple[int, int], str]:
    cand = d.apply(*pos)
    pos_c, cand_c = coords[pos], coords[cand]
    if pos_c == '#':
        return coords
    if pos in coords and cand in coords:
        if can_move(d, pos, coords):
            if cand_c == '.':
                coords[pos] = '.'
                coords[cand] = pos_c
            elif cand_c in '[]':
                bxs = find_boxes(cand, d, coords)
                coords = push(d, bxs, coords)
                # update sprite
                coords[pos] = '.'
                coords[cand] = pos_c
    return coords


def compute(s: str) -> int:

    def scale_up_map(s: str) -> str:
        return (
            s.replace('#', '##')
            .replace('O', '[]')
            .replace('.', '..')
            .replace('@', '@.')
        )

    dmap = {
        '^': support.Direction4.UP,
        '>': support.Direction4.RIGHT,
        'v': support.Direction4.DOWN,
        '<': support.Direction4.LEFT,
    }

    coords_s, moves_s = s.split('\n\n')
    coords_s = scale_up_map(coords_s)
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

    return sum(
        100 * y + x for x, y in coords
        if coords[(x, y)] == '['
    )


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
EXPECTED = 9021


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
