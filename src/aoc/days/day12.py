#!/usr/bin/env python3
from __future__ import annotations

import itertools
import re
import string
from copy import deepcopy
from dataclasses import dataclass, replace

from aoc.utils import run_solution

DAY = 12

type t_grid = list[list[str]]

N = 3

letter_gen = itertools.cycle(string.ascii_uppercase)


@dataclass
class Region:
    x: int
    y: int
    requirements: list[int]

    def grid(self) -> list[list[str]]:
        return [['.'] * self.x for _ in range(self.y)]


def parse_input(data: str):
    lines = data.splitlines()

    shapes: list[t_grid] = []
    regions: list[Region] = []

    parsing_present = False
    acc = []
    for line in lines:
        if re.match(r'\d+:', line):
            parsing_present = True
            continue

        if line == '':
            shapes.append(acc)
            parsing_present = False
            acc = []
            continue

        if parsing_present:
            acc.append(line)
            continue

        parsed = re.search(r'(\d+)x(\d+): (.+)', line)
        if parsed:
            regions.append(Region(
                x=int(parsed.group(1)),
                y=int(parsed.group(2)),
                requirements=list(map(int, parsed.group(3).split(' '))))
            )

    return shapes, regions


def rotate(shape: t_grid) -> t_grid:
    result = []
    for x in range(N):
        result.append(''.join(map(lambda s: s[N - x - 1], shape)))
    return result


def flip(shape: t_grid) -> t_grid:
    return shape[::-1]


def shape_id(shape: t_grid) -> str:
    return ''.join(map(''.join, shape))


def get_variants(shape: t_grid) -> list[t_grid]:
    result = []
    current = shape.copy()
    for _ in range(4):
        current = rotate(current)
        result.extend([current, flip(current)])

    return list({shape_id(s): s for s in result}.values())


def get_taken_space(shape: t_grid) -> int:
    return sum(sum(map(lambda ch: 0 if ch == '.' else 1, l)) for l in shape)


def get_next_shape_index(current, requirements) -> int | None:
    for i in range(current + 1, len(requirements)):
        if requirements[i] > 0:
            return i
    return None


@dataclass
class Frame:
    x: int
    y: int
    shape_index: int
    variant_index: int
    requirements: list[int]
    grid: t_grid

    def all_satisfied(self) -> bool:
        return all(r == 0 for r in self.requirements)

    def can_apply(self, shape_sizes: list[int]) -> bool:
        return self._free_space() >= sum([shape_sizes[i] * k for i, k in enumerate(self.requirements)])

    def is_valid_y(self) -> bool:
        return self.y <= len(self.grid) - N

    def is_shape_applicable(self, shape: t_grid) -> bool:
        if not self._is_valid_shape():
            return False

        result = True
        for x in range(N):
            for y in range(N):
                if shape[y][x] == '#' and self.grid[self.y + y][self.x + x] != '.':
                    result = False
        return result

    def apply_shape(self, shape: t_grid) -> Frame:
        new_grid = deepcopy(self.grid)

        letter = next(letter_gen)

        for x in range(N):
            for y in range(N):
                if shape[y][x] == '#':
                    new_grid[self.y + y][self.x + x] = letter

        new_requirements = self.requirements.copy()
        new_requirements[self.shape_index] = new_requirements[self.shape_index] - 1

        first_shape_index = get_next_shape_index(-1, new_requirements) or 0

        if self.x < len(self.grid[0]) - N:
            return replace(self, x=self.x + 1, grid=new_grid, requirements=new_requirements,
                           shape_index=first_shape_index, variant_index=0)

        else:  # new line
            return replace(self, y=self.y + 1, x=0, grid=new_grid, requirements=new_requirements,
                           shape_index=first_shape_index,
                           variant_index=0)

    def next(self, variants_of_current_shape: int, shape_size: int) -> Frame | None:
        if self._has_space():
            if (self._is_valid_shape()
                    and self._has_enough_space(shape_size)
                    and self.variant_index < variants_of_current_shape - 1):  # try next variant
                return replace(self, variant_index=self.variant_index + 1)

            # try next shape
            next_shape_index = get_next_shape_index(self.shape_index, self.requirements)
            if next_shape_index:
                return replace(self, shape_index=next_shape_index, variant_index=0)

        first_shape_index = get_next_shape_index(-1, self.requirements)
        if first_shape_index is None:
            return None

        # place no shape here and go to the next point
        if self.x < len(self.grid[0]) - N:  # shift right
            return replace(self, shape_index=first_shape_index, variant_index=0, x=self.x + 1)

        if self.y < len(self.grid) - N:  # shift down
            return replace(self, shape_index=first_shape_index, variant_index=0, x=0, y=self.y + 1)

        # nowhere to shift, no next frame
        return None

    def _free_space(self) -> int:
        result = 0
        for y in range(self.y, len(self.grid)):
            for x in range(0, len(self.grid[0])):
                if self.grid[y][x] == '.':
                    result += 1
        return result

    def _is_valid_shape(self) -> bool:
        return self.requirements[self.shape_index] > 0

    def _has_enough_space(self, shape_size: int) -> bool:
        free_space = 0
        for y in range(self.y, self.y + N):
            for x in range(self.x, self.x + N):
                if self.grid[y][x] == '.':
                    free_space += 1

        return free_space >= shape_size

    def _has_space(self) -> bool:
        return (any(p == '.' for p in self.grid[self.y][self.x:self.x + N]) and
                any(p == '.' for p in [self.grid[y][self.x] for y in range(self.y, self.y + N)]))


def can_fit(region: Region, shapes: list[list[t_grid]], shape_sizes: list[int]) -> bool:
    stack = [
        Frame(
            x=0,
            y=0,
            shape_index=0,
            variant_index=0,
            requirements=region.requirements,
            grid=region.grid().copy(),
        )
    ]

    while stack:
        frame = stack.pop()

        if frame.all_satisfied():  # found solution!
            return True

        if not frame.is_valid_y():
            continue

        if not frame.can_apply(shape_sizes):
            continue

        # generate "next" stack frame for backtracking
        next_frame = frame.next(
            variants_of_current_shape=len(shapes[frame.shape_index]),
            shape_size=shape_sizes[frame.shape_index]
        )

        if next_frame:
            stack.append(next_frame)

        # try applying current suggestion
        shape = shapes[frame.shape_index][frame.variant_index]
        if frame.is_shape_applicable(shape):
            # generate stack frame with the shape applied
            new_frame = frame.apply_shape(shape)
            stack.append(new_frame)

    return False


def part1(data: str) -> int:
    shapes, regions = parse_input(data)
    variants: list[list[t_grid]] = list(map(get_variants, shapes))
    shape_sizes: list[int] = list(map(get_taken_space, shapes))

    return sum(map(lambda r: 1 if can_fit(r, variants, shape_sizes) else 0, regions))


def part2(data: str) -> str:
    return "⭐"


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
