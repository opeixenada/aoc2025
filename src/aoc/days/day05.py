#!/usr/bin/env python3
from aoc.utils import run_solution

DAY = 5


def parse_input(data: str) -> tuple[list[range], list[int]]:
    lines = data.splitlines()
    i = lines.index("")

    def parse_range(s: str) -> range:
        xs = [int(x) for x in s.split("-")]
        return range(xs[0], xs[1] + 1)

    fresh_ranges = [parse_range(r) for r in lines[:i]]
    ingredients = [int(x) for x in lines[i + 1:]]

    return fresh_ranges, ingredients


def part1(data: str) -> int:
    fresh_ranges, ingredients = parse_input(data)

    return sum(1
               for i in ingredients
               if any(i in r for r in fresh_ranges))


def part2(data: str) -> int:
    fresh_ranges, _ = parse_input(data)

    def merge(acc: int, ranges: list[range]) -> int:
        if not ranges:
            return acc

        head = ranges[0]
        tail = ranges[1:]

        i = 0
        for r in tail:
            if head.start <= r.start <= head.stop or r.start <= head.start <= r.stop:
                return merge(acc, [*tail[:i], *tail[i + 1:], range(min(head.start, r.start), max(head.stop, r.stop))])
            i += 1

        return merge(acc + len(head), tail)

    return merge(0, fresh_ranges)


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
