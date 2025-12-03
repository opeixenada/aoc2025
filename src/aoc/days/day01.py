#!/usr/bin/env python3
from functools import reduce

from aoc.utils import run_solution

DAY = 1


def parse_input(data: str) -> list[int]:
    return [(1 if line[0] == "R" else -1) * int(line[1:]) for line in data.splitlines()]


def part1(data: str) -> int:
    def foldFunction(acc: tuple[int, int], instruction: int) -> tuple[int, int]:
        next = (acc[0] + instruction) % 100
        return (next, acc[1] + (1 if (next == 0) else 0))

    result = reduce(lambda acc, i: foldFunction(acc, i), parse_input(data), (50, 0))
    return result[1]


def part2(data: str) -> int:
    def foldFunction(acc: tuple[int, int], instruction: int) -> tuple[int, int]:
        x = acc[0] + instruction
        next = x % 100

        zeros_in_instruction = abs(x) // 100
        zeros_in_sign_difference = (
            1 if (acc[0] > 0 and x <= 0 or acc[0] < 0 and x >= 0) else 0
        )

        return (next, acc[1] + zeros_in_instruction + zeros_in_sign_difference)

    result = reduce(lambda acc, i: foldFunction(acc, i), parse_input(data), (50, 0))
    return result[1]


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
