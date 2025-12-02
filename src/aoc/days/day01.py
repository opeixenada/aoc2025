#!/usr/bin/env python3
from functools import reduce

from aoc.utils import read_input


def parse_input(data: str) -> list[int]:
    return [(1 if line[0] == "R" else -1) * int(line[1:]) for line in data.split("\n")]


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


def main():
    DAY = 1

    print(f"=== Advent of Code 2025 - Day {DAY} ===\n")

    # Test with example input
    print("Testing with example input:")
    example_data = read_input(day=DAY, example=True)
    print(f"Part 1: {part1(example_data)}")
    print(f"Part 2: {part2(example_data)}")

    print("\n" + "-" * 40 + "\n")

    # Solve with real input
    print("Solving with real input:")
    input_data = read_input(day=DAY)
    print(f"Part 1: {part1(input_data)}")
    print(f"Part 2: {part2(input_data)}")


if __name__ == "__main__":
    main()
