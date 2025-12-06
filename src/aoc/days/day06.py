#!/usr/bin/env python3
import re
from functools import reduce
from operator import add, mul
from typing import Callable

from aoc.utils import run_solution

DAY = 6


def parse_input(data: str) -> list[str]:
    return data.splitlines()


def get_operation_and_identity(op_char: str) -> tuple[Callable[[int, int], int], int]:
    return (mul, 1) if op_char == '*' else (add, 0)


def part1(data: str) -> int:
    def reduce_tuple(t: tuple[str]) -> int:
        operation, zero = get_operation_and_identity(t[-1])
        return reduce(operation, [int(x) for x in t[:-1]], zero)

    return sum([reduce_tuple(t) for t in list(zip(*[line.split() for line in parse_input(data)]))])


def part2(data: str) -> int:
    parsed = parse_input(data)

    meta = [
        (m.group(1), len(m.group(0)) - 1)
        for m in re.finditer(r'(.)\s*', parsed[-1] + ' ')
        if m.group(0)
    ]

    def split_by_meta(xs: str) -> list[str]:
        return reduce(
            lambda acc, m: (acc[0] + [xs[acc[1]:acc[1] + m[1]]], acc[1] + m[1] + 1),
            meta, ([], 0)
        )[0]

    def reduce_by_meta(t: tuple) -> int:
        op_char, k = t[-1]
        op, zero = get_operation_and_identity(op_char)
        nums = [int(''.join(elem[i] for elem in t[:-1])) for i in range(k)]
        return reduce(op, nums, zero)

    return sum(map(reduce_by_meta, zip(*map(split_by_meta, parsed[:-1]), meta)))


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
