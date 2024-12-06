from __future__ import annotations

import argparse
import os.path
import re

import pytest
from z3 import Int
from z3 import Ints
from z3 import sat
from z3 import Solver

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def check_order(lst: list[int], orders: list[tuple[int, ...]]) -> bool:
    return all(
        lst.index(first) < lst.index(second)
        for first, second in orders
        if first in lst and second in lst
    )


def compute(s: str) -> int:
    total = 0
    ordering, updates = s.split('\n\n')
    orders = list(
        tuple(map(int, order.split('|')))
        for order in ordering.splitlines()
    )
    incorrect_lsts = []

    for update in updates.splitlines():
        lst = list(map(int, update.split(',')))
        if not check_order(lst, orders):
            incorrect_lsts.append(lst)

    for lst in incorrect_lsts:
        so = Solver()
        for x, y in orders:
            if x in lst and y in lst:
                ox, oy = Ints(f'o{x} o{y}')
                so.add(0 <= ox)
                so.add(ox < oy)

        for elem in lst:
            e = Int(f'o{elem}')
            so.add(0 <= e)
            so.add(e < len(lst))

        if so.check() == sat:
            m = so.model()

            correct_order = sorted(
                [
                    tuple(map(int, m.groups()))
                    for m in re.finditer(r'o(\d+) = (\d+)', str(m))
                ],
                key=lambda x: x[1],
            )
            total += [x[0] for x in correct_order][len(lst) // 2]

    return total


INPUT_S = '''\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''
EXPECTED = 123


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
