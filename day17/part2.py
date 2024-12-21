from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def do(registers: tuple[int, int, int]) -> list[int]:
    A, B, C = registers
    output = []
    while A != 0:
        B = (A % 8) ^ 1
        C = A // (2 ** B)
        B = (B ^ 5) ^ C
        A = A // 8

        output.append(B % 8)
    # print(f'{A=}, {B=}, {C=}, output={output}')
    return output


def compute(s: str) -> int:
    _, program_s = s.split('\n\n')
    _, rest = program_s.split(': ')
    program = tuple(int(c) for c in rest.split(','))
    a = 164541017976449  # start after trying 8 ** 15

    while a <= 8 ** 16:
        output = do((a, 0, 0))
        if output == list(program):
            break
        a += 1
    return a


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
