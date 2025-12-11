#!/usr/bin/env python3
from functools import reduce
from itertools import combinations
from math import sqrt

from aoc.utils import run_solution

DAY = 8


def parse_input(data: str) -> tuple[list[set[str]], list[tuple[float, str, str]]]:
    parsed = [[int(s) for s in line.split(',')] for line in data.splitlines()]

    circuits: list[set[str]] = [{box_id(box)} for box in parsed]

    distances = [(distance(a, b), box_id(a), box_id(b)) for a, b in combinations(parsed, 2)]
    distances.sort(key=lambda x: x[0])

    return circuits, distances


def box_id(box: list[int]) -> str:
    return ','.join(map(str, box))


def distance(a: list[int], b: list[int]):
    return sqrt(sum([(x - y) ** 2 for (x, y) in zip(a, b)]))


def merge(xs: list[set[str]], a: str, b: str) -> list[set[str]]:
    i = [i for i, x in enumerate(xs) if a in x][0]
    j = [i for i, x in enumerate(xs) if b in x][0]
    return [*xs[:min(i, j)], *xs[min(i, j) + 1:max(i, j)], *xs[max(i, j) + 1:], xs[i].union(xs[j])]


def part1(data: str) -> int:
    connections = 1000

    def score(xs: list[set[str]]) -> int:
        sizes = [len(x) for x in xs]
        sizes.sort(reverse=True)
        return reduce(lambda a, b: a * b, sizes[:3], 1)

    circuits, distances = parse_input(data)

    return score(reduce(lambda acc, t: merge(acc, t[1], t[2]), distances[:connections], circuits))


def part2(data: str) -> int:
    circuits, distances = parse_input(data)

    i = -1
    while len(circuits) > 1:
        i += 1
        _, a, b = distances[i]
        circuits = merge(circuits, a, b)

    _, a, b = distances[i]

    def get_x(box: str) -> int:
        return int(box.split(",")[0])

    return get_x(a) * get_x(b)


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
