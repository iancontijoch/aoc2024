from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def do(
        program: tuple[int, ...],
        registers: dict[str, int],
        combo: dict[int, int],
        pointer: int,
) -> tuple[list[int], dict[str, int], dict[int, int], int]:

    increase_pointer = True
    output = []
    opcode = program[pointer]
    operand = program[pointer + 1]

    if opcode == 0:
        registers['A'] = registers['A'] // (2 ** combo[operand])
    elif opcode == 1:
        registers['B'] = registers['B'] ^ operand
    elif opcode == 2:
        registers['B'] = combo[operand] % 8
    elif opcode == 3:
        if registers['A'] != 0:
            pointer = operand
            increase_pointer = False
    elif opcode == 4:
        registers['B'] = registers['B'] ^ registers['C']
    elif opcode == 5:
        output.append(combo[operand] % 8)
    elif opcode == 6:
        registers['B'] = registers['A'] // (2 ** combo[operand])
    elif opcode == 7:
        registers['C'] = registers['A'] // (2 ** combo[operand])
    else:
        raise ValueError('Did not recognize instruction')

    combo = get_combo(registers)
    return output, registers, combo, pointer + (increase_pointer * 2)


def get_combo(registers: dict[str, int]) -> dict[int, int]:
    return {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: registers['A'],
        5: registers['B'],
        6: registers['C'],
    }


def get_program_output(
    program: tuple[int, ...],
    registers: dict[str, int],
) -> tuple[list[int], dict[str, int]]:
    pointer = 0
    outputs = []
    combo = get_combo(registers)
    while pointer < len(program):
        output, registers, combo, pointer = do(
            program, registers, combo, pointer,
        )
        outputs.extend(output)
    return outputs, registers


def compute(s: str) -> int:
    registers_s, program_s = s.split('\n\n')
    registers = dict(zip('ABC', map(int, re.findall(r'\d+', registers_s))))
    _, rest = program_s.split(': ')
    program = tuple(int(c) for c in rest.split(','))
    A = 0
    i = 0

    while True:
        if i % 100_000 == 0:
            print(A, i)
        output, registers = get_program_output(program, registers)
        if output == list(program):
            break
        A += 8
        registers['A'] = A
        i += 1
    return A


INPUT_S = '''\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
'''
EXPECTED = 117440


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
