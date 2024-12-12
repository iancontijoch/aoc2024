from __future__ import annotations

import argparse
import itertools
import os.path
from typing import cast

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Block():

    def __init__(self, value: str, index: int, length: int):
        self.value = value
        self.index = index
        self.length = length
        self.erased: bool = False

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(value=\'{self.value}\','
            f'index={self.index}, length={self.length},'
            f' erased={self.erased})'
        )


class Space(Block):
    def __init__(self, value: str, index: int, length: int):
        super().__init__(value=value, index=index, length=length)
        self.free_space = length
        self.files: list[Block] = []

    def __repr__(self) -> str:
        return super().__repr__() + (
            f'(free_space={self.free_space}, files={self.files})'
        )


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        numbers = list(map(int, line))
        files = ([str(i)] * n for i, n in enumerate(numbers[::2]))
        free_space = (['.'] * n for n in numbers[1::2])
        block_lst = [
            c for c in
            itertools.chain(
                *itertools.zip_longest(files, free_space),
            )
            if c is not None
        ]
        blocks = tuple(
            Block(value=x[0], index=i, length=len(x))
            if x[0] != '.' else Space(x[0], i, len(x))
            for i, x in enumerate(block_lst) if x
        )

        file_blocks = tuple(block for block in blocks if block.value != '.')
        space_blocks = tuple(block for block in blocks if block.value == '.')

        state = {block.index: block for block in blocks}

        for file_block in reversed(file_blocks):
            for space_block in space_blocks:
                if (
                    not isinstance(space_block, Space)
                    or not isinstance(state[space_block.index], Space)
                ):
                    raise ValueError

                state_space_block = cast(Space, state[space_block.index])

                if (
                    space_block.index < file_block.index
                    and space_block.free_space >= file_block.length
                ):  # has slot
                    state_space_block.files.append(file_block)
                    state_space_block.free_space -= file_block.length
                    state[file_block.index].erased = True
                    break
        res = []
        for block in state.values():
            if isinstance(block, Space):
                res += [
                    [f.value] * f.length
                    for f in block.files
                ] + ['.'] * block.free_space
            else:
                res += block.length * [
                    [block.value]
                    if not block.erased else '.',
                ]
        flattened_lst = [x for y in res for x in y]
        total += sum(
            i * int(c)
            for i, c in enumerate(flattened_lst)
            if c != '.'
        )
    return total


INPUT_S = '''\
2333133121414131402
'''

EXPECTED = 2858


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
