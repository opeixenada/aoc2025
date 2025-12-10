#!/usr/bin/env python3
from functools import reduce

from aoc.utils import run_solution

DAY = 7


def parse_input(data: str) -> tuple[int, list[set[int]]]:
    lines = data.splitlines()
    start = lines[0].index('S')
    manifold = [set([i for i, c in enumerate(line) if c == '^']) for line in lines[1:]]
    return start, manifold


def part1(data: str) -> int:
    (start, manifold) = parse_input(data)

    def reduce_manifold(acc: tuple[int, set[int]], line: set[int]) -> tuple[int, set[int]]:
        count, beams = acc
        return reduce(
            lambda a, beam:
            (a[0] + 1, a[1].union({beam - 1, beam + 1})) if beam in line
            else (a[0], a[1].union({beam})),
            beams, (count, set()))

    return reduce(reduce_manifold, manifold, (0, {start}))[0]


type weighted_beam = tuple[int, int]  # x coordinate, weight 


def part2(data: str) -> int:
    (start, manifold) = parse_input(data)

    def reduce_manifold(acc: dict[int, int], line: set[int]) -> dict[int, int]:
        return reduce(
            lambda next_beams, x:
            {**next_beams, x: next_beams.get(x, 0) + acc[x]} if x not in line
            else {**next_beams,
                  x - 1: next_beams.get(x - 1, 0) + acc[x],
                  x + 1: next_beams.get(x + 1, 0) + acc[x]},
            acc.keys(),
            {}
        )

    return sum(reduce(reduce_manifold, manifold, {start: 1}).values())


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
