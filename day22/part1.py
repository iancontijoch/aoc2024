from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def mix(value: int, secret_number: int) -> int:
    return value ^ secret_number


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def price(secret_number: int) -> int:
    secret_number = prune(mix((secret_number * 64), secret_number))
    secret_number = prune(mix((secret_number // 32), secret_number))
    return prune(mix(secret_number * 2048, secret_number))


def compute(s: str) -> int:
    total = 0
    numbers = support.parse_numbers_split(s)
    for n in numbers:
        secret_number = n
        for _ in range(2000):
            secret_number = price(secret_number)
        total += secret_number
    return total


INPUT_S = '''\
1
10
100
2024
'''
EXPECTED = 37327623


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
