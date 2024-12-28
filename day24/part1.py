from __future__ import annotations

import argparse
import operator
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OPS = {
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor,
}


def compute(s: str) -> int:
    inputs_s, connections_s = s.split('\n\n')
    wires = {
        wire: int(n)
        for wire, n in (
            line.split(': ')
            for line in inputs_s.splitlines()
        )
    }

    todo: deque[tuple[str, ...]] = deque()
    for line in connections_s.splitlines():
        gates, out = line.split(' -> ')
        todo.append(tuple(gates.split() + [out]))

    while todo:
        g1, op_s, g2, out = todo.popleft()
        if g1 not in wires or g2 not in wires:
            todo.append((g1, op_s, g2, out))
            continue
        op = OPS[op_s]
        wires[out] = op(wires[g1], wires[g2])

    z_wires = ((k, v) for k, v in wires.items() if k[0] == 'z')
    return int(
        ''.join(
            str(x[1])
            for x in sorted(z_wires, reverse=True)
        ), 2,
    )


INPUT_S_1 = '''\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
'''
EXPECTED_1 = 4


INPUT_S_2 = '''\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''
EXPECTED_2 = 2024


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
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
