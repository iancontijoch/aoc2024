from __future__ import annotations

import argparse
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    _, connections_s = s.split('\n\n')

    todo = []
    for line in connections_s.splitlines():
        gates, out = line.split(' -> ')
        todo.append(tuple(gates.split() + [out]))

    wrong = set()

    # first 6 swaps
    for inst in todo:
        g1, op_s, g2, out = inst
        if out[0] == 'z' and out != 'z45' and op_s != 'XOR':
            wrong.add(inst)
        if (
            out[0] != 'z'
            and g1[0] not in 'xy'
            and g2[0] not in 'xy'
            and op_s == 'XOR'
        ):
            wrong.add(inst)

    # last 2 swaps
    for inst in todo:
        if inst not in wrong:
            g1, op_s, g2, out = inst
            if op_s == 'XOR':
                if (
                    g1[0] in 'xy'
                    and g2[0] in 'xy'
                    and 'y00' not in (g1, g2)
                    and 'x001' not in (g1, g2)
                ):
                    crit1 = [
                        inst for inst in todo
                        if inst[1] == 'XOR'
                        and (inst[0] == out or inst[2] == out)
                    ]
                    if not crit1:
                        wrong.add(inst)
            if op_s == 'AND':
                if (
                    g1[0] in 'xy'
                    and g2[0] in 'xy'
                    and 'y00' not in (g1, g2)
                    and 'x001' not in (g1, g2)
                ):
                    crit2 = [
                        inst for inst in todo
                        if inst[1] == 'OR'
                        and (inst[0] == out or inst[2] == out)
                    ]
                    if not crit2:
                        wrong.add(inst)

    return ','.join(sorted(w[-1] for w in wrong))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
