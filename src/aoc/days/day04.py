#!/usr/bin/env python3
from aoc.utils import run_solution

DAY = 4


def parse_input(data: str) -> list[list[bool]]:
    return [[char == '@' for char in line] for line in data.splitlines()]


def accessible(grid: list[list[bool]], removed: set[tuple[int, int]]) -> set[tuple[int, int]]:
    def is_accessible(x: int, y: int) -> bool:
        if not grid[y][x] or (x, y) in removed:
            return False

        return sum(
            1
            for i in range(max(0, x - 1), min(x + 2, len(grid)))
            for j in range(max(0, y - 1), min(y + 2, len(grid)))
            if grid[j][i] and (i, j) not in removed
        ) < 5

    return set(
        (x, y)
        for x in range(len(grid[0]))
        for y in range(len(grid))
        if is_accessible(x, y)
    )


def part1(data: str) -> int:
    return len(accessible(parse_input(data), set()))


def part2(data: str) -> int:
    grid = parse_input(data)

    def remove_rolls(removed: set[tuple[int, int]]) -> set[tuple[int, int]]:
        accessible_rolls = accessible(grid, removed)
        if accessible_rolls:
            return remove_rolls(removed | accessible_rolls)
        return removed

    return len(remove_rolls(set()))


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
