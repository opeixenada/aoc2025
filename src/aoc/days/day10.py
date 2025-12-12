#!/usr/bin/env python3
import re
from dataclasses import dataclass
from functools import reduce
from itertools import zip_longest

from aoc.utils import run_solution

DAY = 10


def bit_mask(xs: list[int]) -> int:
    return reduce(lambda mask, x: mask | (1 << x), xs, 0)


def permutations(n: int, target: int) -> list[list[int]]:
    if n == 0:
        return [[]] if target == 0 else []

    result = []
    for k in range(target + 1):
        tail = permutations(n - 1, target - k)
        result.extend([k] + t for t in tail)

    return result


def apply_buttons(buttons: list[list[int]], permutation: list[int], x: list[int]) -> list[int]:
    result = x
    for button, k in zip(buttons, permutation):
        result = [v + b * k for v, b in zip(result, button)]
    return result


@dataclass
class State:
    lights: list[int]
    buttons: list[list[int]]
    count: int


@dataclass
class Machine:
    indicators: int
    buttons: list[list[int]]
    joltage: list[int]

    def set_indicators(self) -> int:
        buttons_binary = list(map(bit_mask, self.buttons))
        states = {0}
        i = 1
        while True:
            new_states = set()
            for state in states:
                for button in buttons_binary:
                    s = state ^ button
                    if s == self.indicators:
                        return i
                    new_states.add(s)
            states = new_states
            i += 1

    def list_mask(self, xs: list[int]) -> list[int]:
        return reduce(lambda ys, x: list(map(sum, zip_longest(ys, ([0] * x) + [1], fillvalue=0))), xs,
                      [0] * len(self.joltage))

    def is_valid_joltage(self, joltage: list[int]) -> bool:
        return all(a <= b for (a, b) in zip(joltage, self.joltage))

    def set_joltage(self) -> int:
        buttons_masks = list(map(self.list_mask, self.buttons))
        stack = [State(lights=[0] * len(self.joltage), buttons=buttons_masks, count=0)]
        result: int = 0

        i = -1

        # DFS
        while True:
            i += 1

            if not stack:
                print(f"> {result}!")
                return result

            print(f"stack: {len(stack)}")

            s = stack.pop()

            # find the smallest gap between target and current joltage values
            targets = list(
                filter(
                    lambda t: t[1] > 0,
                    enumerate(map(lambda t: t[1] - t[0], zip(s.lights, self.joltage)))
                )
            )

            if not targets:
                if not result:
                    result = s.count
                else:
                    result = min(result, s.count)

                print(f">> {result}?")
                continue

            targets.sort(key=lambda x: x[1])
            (index, target) = targets[0]

            if result and s.count + targets[-1][1] >= result:
                print(f"{i} EXC")
                continue

            # find all the buttons that can reach the target, they should be pressed `target` times in total
            relevant_buttons = list(filter(lambda b: b[index] == 1, s.buttons))
            other_buttons = list(filter(lambda b: b[index] == 0, s.buttons))

            # distribute `target` between those buttons
            relevant_buttons_permutations: list[list[int]] = permutations(len(relevant_buttons), target)

            # apply buttons
            new_lights = filter(self.is_valid_joltage,
                                [apply_buttons(relevant_buttons, permutation, s.lights) for permutation in
                                 relevant_buttons_permutations])
            
            if not other_buttons:
                if any(lights == self.joltage for lights in new_lights):
                    if not result:
                        result = s.count + target
                    else:
                        result = min(result, s.count + target)

                    print(f">> {result}?")
                    continue
            
            new_states = [State(lights=lights, buttons=other_buttons, count=s.count + target) for lights in
                          new_lights]

            stack.extend(new_states)


def parse_input(data: str) -> list[Machine]:
    def parse_line(line: str) -> Machine:
        parsed = re.search(r"\[(.*)] (\(.*\))+ (\{.*})", line)

        if parsed:
            indicators = ''.join(['0' if ch == '.' else '1' for ch in parsed.group(1)[::-1]])

            return Machine(
                indicators=int(indicators, 2),
                buttons=[[int(n) for n in button[1:-1].split(',')] for button in
                         parsed.group(2).split(' ')],
                joltage=[int(n) for n in parsed.group(3)[1:-1].split(',')]
            )

        raise Exception(f"Can't parse `{line}`")

    return list(map(parse_line, data.splitlines()))


def part1(data: str) -> int:
    return sum([m.set_indicators() for m in parse_input(data)])


def part2(data: str) -> int:
    return sum([m.set_joltage() for m in parse_input(data)])


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
