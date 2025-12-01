#!/usr/bin/env python3
from aoc.utils import read_input


def parse_input(data: str):
    lines = data.split("\n")
    # TODO: Parse your input here
    return lines


def part1(data: str) -> int:
    parsed = parse_input(data)
    # TODO: Implement part 1 solution
    return 0


def part2(data: str) -> int:
    parsed = parse_input(data)
    # TODO: Implement part 2 solution
    return 0


def main():
    # Update this to the current day
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
