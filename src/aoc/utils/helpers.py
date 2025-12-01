"""
Common utility functions for Advent of Code solutions.
"""

from pathlib import Path


def read_input(day: int, example: bool = False) -> str:
    """Read input file for a given day.

    Returns:
        The input file contents as a string
    """
    filename = f"day{day:02d}_example.txt" if example else f"day{day:02d}.txt"
    input_path = Path(__file__).parent.parent.parent.parent / "inputs" / filename
    return input_path.read_text().strip()
