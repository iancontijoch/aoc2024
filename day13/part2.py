from __future__ import annotations

import argparse
import os.path
import re

import pytest
from z3 import Ints
from z3 import Optimize
from z3 import sat

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

COST_A, COST_B = 3, 1
OFFSET = 10000000000000


def compute(s: str) -> int:
    total = 0
    configs = s.split('\n\n')
    for config in configs:
        a_s, b_s, p_s = config.splitlines()

        a_x, a_y = tuple(map(int, re.findall(r'\d+', a_s)))
        b_x, b_y = tuple(map(int, re.findall(r'\d+', b_s)))
        p_x, p_y = tuple(map(int, re.findall(r'\d+', p_s)))

        p_x += OFFSET
        p_y += OFFSET

        o = Optimize()
        n_a, n_b = Ints('n_a n_b')
        total_cost = COST_A * n_a + COST_B * n_b

        o.add(
            0 <= n_a,
            0 <= n_b,
            n_a * a_x + n_b * b_x == p_x,
            n_a * a_y + n_b * b_y == p_y,
        )
        o.minimize(total_cost)
        if o.check() == sat:
            m = o.model()
            total += COST_A * m[n_a].as_long() + COST_B * m[n_b].as_long()

    return total


INPUT_S = '''\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''
EXPECTED = 480


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
