from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    lines = s.splitlines()
    graph = defaultdict(list)

    max_cluster_size = 0
    max_nodes = []

    for line in lines:
        v1, v2 = line.split('-')
        graph[v1].append(v2)
        graph[v2].append(v1)

    clusters: dict[str, dict[int, list[str]]] = defaultdict(dict)
    for node in graph:
        overlaps = defaultdict(list)
        seen = {node}
        neighbors = graph[node]
        seen.update(neighbors)
        for neighbor in neighbors:
            overlap_size = len(set(graph[neighbor]) & set(seen))
            overlaps[overlap_size].append(neighbor)
        clusters[node] = overlaps

    for node, cluster in clusters.items():
        for cluster_size, nodes in cluster.items():
            if cluster_size == len(nodes) and cluster_size > max_cluster_size:
                max_nodes = nodes + [node]
                max_cluster_size = cluster_size

    return ','.join(sorted(max_nodes))


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
EXPECTED = 'co,de,ka,ta'


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
