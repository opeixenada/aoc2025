"""
Common utility functions for Advent of Code solutions.
"""

from pathlib import Path
from typing import Any, Callable


def read_input(day: int, example: bool = False) -> str:
    """Read input file for a given day.

    Returns:
        The input file contents as a string
    """
    filename = f"day{day:02d}_example.txt" if example else f"day{day:02d}.txt"
    input_path = Path(__file__).parent.parent.parent.parent / "inputs" / filename
    return input_path.read_text()


def run_solution(day: int, part1: Callable[[str], Any], part2: Callable[[str], Any]) -> None:
    """Run both parts of a solution with example and real input.

    Args:
        day: The day number (1-25)
        part1: Function that solves part 1, takes input string and returns any type
        part2: Function that solves part 2, takes input string and returns any type
    """
    print(f"=== Advent of Code 2025 - Day {day} ===\n")
    
    # Test with example input
    print("Testing with example input:")
    example_data = read_input(day=day, example=True)
    print(f"Part 1: {part1(example_data)}")
    print(f"Part 2: {part2(example_data)}")
    
    print("\n" + "-" * 40 + "\n")
    
    # Solve with real input
    print("Solving with real input:")
    input_data = read_input(day=day)
    print(f"Part 1: {part1(input_data)}")
    print(f"Part 2: {part2(input_data)}")
