#!/usr/bin/env python3
from aoc.utils import run_solution

DAY = 3


def parse_input(data: str) -> list[list[int]]:
    return [list(map(int, line)) for line in data.splitlines()]


def part1(data: str) -> int:
    def max_joltage(bank: list[int]) -> int:
        return max_joltage_rec(bank[0], bank[1], bank[2:])

    def max_joltage_rec(a: int, b: int, rest: list[int]) -> int:
        if not rest:
            return a * 10 + b

        c = rest[0]
        tail = rest[1:]
        if b > a:
            return max_joltage_rec(b, c, tail)
        if c > b:
            return max_joltage_rec(a, c, tail)
        return max_joltage_rec(a, b, tail)

    return sum(map(max_joltage, parse_input(data)))


def part2(data: str) -> int:
    def max_joltage(bank: list[int]) -> int:
        return max_joltage_rec(bank[:12], bank[12:])

    def max_joltage_rec(selected: list[int], rest: list[int]) -> int:
        if not rest:
            return int(''.join(map(str, selected)))

        selected.append(rest[0])
        return max_joltage_rec(rearrange([], selected), rest[1:])

    def rearrange(acc: list[int], rest: list[int]) -> list[int]:
        if len(rest) < 2:
            return acc

        a = rest[0]
        b = rest[1]

        if b > a:
            return [*acc, b, *rest[2:]]

        acc.append(a)
        return rearrange(acc, rest[1:])

    return sum(map(max_joltage, parse_input(data)))


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
