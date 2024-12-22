from __future__ import annotations

import argparse
import os.path
import re
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_num_paths(
    spans: list[tuple[int, int]],
    end: int,
) -> int:
    adj_list = defaultdict(list)
    for a, b in spans:
        adj_list[a].append(b)

    starts = adj_list[0]
    memo: dict[int, int] = {}

    def dfs(node: int) -> int:
        if node in memo:
            return memo[node]

        if node == end:
            return 1

        total_paths = 0
        for neighbor in adj_list[node]:
            total_paths += dfs(neighbor)

        memo[node] = total_paths
        return total_paths

    total_paths = sum(dfs(start) for start in starts)
    return total_paths


def find_spans(blocks: list[str], design: str) -> list[tuple[int, int]]:
    spans = []
    for block in blocks:
        start = 0
        while start < len(design):
            match = re.search(block, design[start:])
            if not match:
                break
            span = (start + match.start(), start + match.end())
            spans.append(span)
            start += match.start() + 1  # Allow overlap
    return spans


def compute(s: str) -> int:
    total = 0
    blocks_s, designs_s = s.split('\n\n')
    blocks = blocks_s.split(', ')
    designs = designs_s.splitlines()

    for design in designs:
        spans = find_spans(blocks, design)
        total += get_num_paths(spans, len(design))
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
EXPECTED = 16


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
