#!/usr/bin/env python3
from aoc.utils import read_input


def parse_input(data: str) -> list[tuple[str, str]]:
    return [(a, b) for id_range in data.split(",") for a, b in [id_range.split("-")]]


def part1(data: str) -> int:
    def get_left(s: str) -> int:
        half = len(s) // 2
        if len(s) % 2 == 0:
            return int(s[:half]) + (1 if s[:half] < s[half:] else 0)
        return 10 ** half

    def get_right(s: str) -> int:
        half = len(s) // 2
        if len(s) % 2 == 0:
            return int(s[:half]) - (1 if s[:half] > s[half:] else 0)
        return 10 ** half - 1

    def invalid_ids_sum(id_range: tuple[str, str]) -> int:
        return sum([int(str(x) * 2) for x in
                    range(get_left(id_range[0]), get_right(id_range[1]) + 1)])

    return sum([invalid_ids_sum(id_range) for id_range in parse_input(data)])


def part2(data: str) -> int:
    def is_invalid(s: str) -> bool:
        n = len(s)
        for size in range(1, n):
            if n % size == 0 and s == s[:size] * (n // size):
                return True
        return False

    def invalid_ids_sum(id_range: tuple[str, str]) -> int:
        return sum([x for x in range(int(id_range[0]), int(id_range[1]) + 1) if is_invalid(str(x))])

    return sum([invalid_ids_sum(id_range) for id_range in parse_input(data)])


def main():
    # Update this to the current day
    DAY = 2

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
