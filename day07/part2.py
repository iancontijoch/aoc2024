from __future__ import annotations

import argparse
import itertools
import operator
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    seen = set()
    total = 0

    for line in lines:
        test_value_s, rest = line.split(':')
        test_value = int(test_value_s)
        numbers = deque(map(int, rest.split()))
        ops_combo = deque(
            itertools.product(
                (operator.mul, operator.add, operator.concat),
                repeat=len(numbers) - 1,
            ),
        )

        while ops_combo:
            q = numbers.copy()
            ops = deque(ops_combo.popleft())
            while q:
                if len(q) == 1:
                    if q.popleft() == test_value and line not in seen:
                        total += test_value
                        seen.add(line)
                else:
                    a, b, op = q.popleft(), q.popleft(), ops.popleft()
                    if op == operator.concat:
                        q.appendleft(int(op(str(a), str(b))))
                    else:
                        q.appendleft(op(a, b))
    return total


INPUT_S = '''\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
EXPECTED = 11387


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
