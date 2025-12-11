#!/usr/bin/env python3
from functools import reduce, lru_cache
from itertools import combinations, filterfalse
from operator import mul

from aoc.utils import run_solution

DAY = 9

type t_point = tuple[int, int]
type t_line = tuple[t_point, t_point]


def parse_input(data: str) -> list[t_point]:
    result = []
    for s in data.splitlines():
        x, y = map(int, s.split(','))
        result.append((x, y))
    return result


def area(t: tuple[t_point, t_point]) -> int:
    a, b = t
    return reduce(mul, ([abs(x - y) + 1 for (x, y) in zip(a, b)]), 1)


def part1(data: str) -> int:
    return max(map(area, combinations(parse_input(data), 2)))


def part2(data: str) -> int:
    red = parse_input(data)

    def is_vertical(l: t_line) -> bool:
        return l[0][0] == l[1][0]

    contour: list[t_line] = list(zip(red, red[1:] + [red[0]]))

    contour_verticals: list[t_line] = [
        ((line[0][0], min(line[0][1], line[1][1])), (line[0][0], max(line[0][1], line[1][1]))) for line in
        filter(is_vertical, contour)]

    contour_horizontals: list[t_line] = [
        ((min(line[0][0], line[1][0]), line[0][1]), (max(line[0][0], line[1][0]), line[0][1])) for line in
        filterfalse(is_vertical, contour)]

    @lru_cache(maxsize=None)
    def is_edge_point(p: t_point) -> bool:
        return any(v[0][1] <= p[1] <= v[1][1] and v[0][0] == p[0] for v in contour_verticals) or any(
            h[0][0] <= p[0] <= h[1][0] and h[0][1] == p[1] for h in contour_horizontals)

    @lru_cache(maxsize=None)
    def is_inner_point(p: t_point) -> bool:
        right_verticals = list(filter(lambda v: v[0][0] > p[0] and v[0][1] < p[1] < v[1][1], contour_verticals))
        right_horizontals = list(filter(lambda h: h[0][0] > p[0] and h[0][1] == p[1], contour_horizontals))
        result = is_edge_point(p) or (len(right_verticals) + len(right_horizontals)) % 2 == 1
        return result

    @lru_cache(maxsize=None)
    def is_inner_line(l: t_line) -> bool:
        if is_vertical(l):
            points = [(l[0][0], y) for y in range(min(l[0][1], l[1][1]), max(l[0][1], l[1][1]) + 1)]
        else:
            points = [(x, l[0][1]) for x in range(min(l[0][0], l[1][0]), max(l[0][0], l[1][0]) + 1)]

        result = all(is_inner_point(p) for p in points)

        return result

    def is_valid_rectangle(t: tuple[t_point, t_point]) -> bool:
        a, b = t

        result = (all(is_inner_point(p) for p in [(a[0], b[1]), (b[0], a[1])]) and
                  all(is_inner_line(line) for line in [
                      (a, (a[0], b[1])),
                      (a, (b[0], a[1])),
                      (b, (a[0], b[1])),
                      (b, (b[0], a[1])),
                  ]))
        return result

    all_rectangles = list(combinations(red, 2))
    all_rectangles.sort(key=area, reverse=True)

    for rect in all_rectangles:
        if is_valid_rectangle(rect):
            return area(rect)

    return 0


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
