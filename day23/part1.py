from __future__ import annotations

import argparse
import itertools
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    graph = defaultdict(list)
    for line in lines:
        v1, v2 = line.split('-')
        graph[v1].append(v2)
        graph[v2].append(v1)

    seen = set()
    for v1, v2, v3 in itertools.combinations(graph, 3):
        if v1 in graph[v2] and v1 in graph[v3]:
            if v2 in graph[v1] and v2 in graph[v3]:
                if v3 in graph[v1] and v3 in graph[v2]:
                    fingerprint = tuple(sorted((v1, v2, v3)))
                    if v1[0] == 't' or v2[0] == 't' or v3[0] == 't':
                        if fingerprint not in seen:
                            seen.add(fingerprint)
                            total += 1
    return total


INPUT_S = '''\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''
EXPECTED = 7


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
