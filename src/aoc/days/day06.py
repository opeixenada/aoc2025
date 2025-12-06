#!/usr/bin/env python3
from functools import reduce
from itertools import takewhile
from typing import Callable

from aoc.utils import run_solution

DAY = 6

type t_meta = list[tuple[str, int]]


def parse_input(data: str) -> list[str]:
    return data.splitlines()


def part1(data: str) -> int:
    def reduce_tuple(t: tuple[str]) -> int:
        operation: Callable[[int, int], int] = (lambda x, y: x * y) if t[-1] == '*' else (lambda x, y: x + y)
        zero: int = 1 if t[-1] == '*' else 0
        return reduce(operation, [int(x) for x in t[:-1]], zero)

    return sum([reduce_tuple(t) for t in list(zip(*[line.split() for line in parse_input(data)]))])


def part2(data: str) -> int:
    parsed = parse_input(data)

    def get_meta(xs: str) -> t_meta:
        acc = []
        i = 0

        while i < len(xs):
            spaces_count = len(list(takewhile(lambda s: s.isspace(), xs[(i + 1):])))
            acc.append((xs[i], spaces_count))
            i += spaces_count + 1

        return acc

    meta = get_meta(parsed[-1] + ' ')

    def split_numbers(xs: str) -> list[str]:
        acc = []
        i = 0
        j = 0

        while i < len(meta):
            k = meta[i][1]
            acc.append(xs[j:(j + k)])
            i += 1
            j += k + 1

        return acc

    def reduce_tuple(t: tuple) -> int:
        operation: Callable[[int, int], int] = (lambda x, y: x * y) if t[-1][0] == '*' else (lambda x, y: x + y)
        zero: int = 1 if t[-1][0] == '*' else 0

        k = t[-1][1]

        numbers = []
        i = 0

        while i < k:
            numbers.append(int(''.join(map(lambda s: s[i], t[:-1]))))
            i += 1

        print(f"{t[-1][0]}: {numbers}")

        return reduce(operation, numbers, zero)

    return sum(map(reduce_tuple, list(zip(*list(map(split_numbers, parsed[:-1])), meta))))


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)

# 12608160007999 too low
