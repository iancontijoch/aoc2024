from __future__ import annotations

import argparse
import heapq
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def can_traverse(spans: list[tuple[int, int]], end: int) -> bool:
    starts = [s for s in spans if s[0] == 0]
    seen = set()

    q = starts
    while q:
        a, b = heapq.heappop(q)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        if b == end:
            return True
        for adj in [s for s in spans if s[0] == b]:
            heapq.heappush(q, adj)
    return False


def is_possible(design: str, blocks: list[str]) -> bool:
    spans = [
        m.span()
        for block in blocks
        for m in re.finditer(pattern=rf'{block}', string=design)
    ]
    return can_traverse(spans, end=len(design))


def compute(s: str) -> int:
    total = 0
    blocks_s, designs_s = s.split('\n\n')
    blocks = blocks_s.split(', ')
    designs = designs_s.splitlines()

    for design in designs:
        if is_possible(design, blocks):
            total += 1
    return total


INPUT_S = '''\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''
EXPECTED = 6


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
