from __future__ import annotations

import argparse
import os.path

import pytest

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

    for update in updates.splitlines():
        lst = list(map(int, update.split(',')))
        if check_order(lst, orders):
            total += lst[len(lst) // 2]
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
EXPECTED = 143


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
