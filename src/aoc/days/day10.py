#!/usr/bin/env python3
import re
from dataclasses import dataclass
from functools import reduce

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD, value

from aoc.utils import run_solution

DAY = 10


def bit_mask(xs: list[int]) -> int:
    return reduce(lambda mask, x: mask | (1 << x), xs, 0)


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

    def set_joltage(self) -> int:
        # For each button, see how many times at most it can be applied
        upper_bounds = []
        for button in self.buttons:
            m = max(self.joltage)
            for n in button:
                m = min(m, self.joltage[n])
            upper_bounds.append(m)

        equalities: list[list[int]] = []
        equalities_rhs: list[int] = []
        for i, jolt in enumerate(self.joltage):
            relevant_buttons: list[int] = list(
                map(
                    lambda b: b[0],
                    filter(lambda b: i in b[1], enumerate(self.buttons))
                )
            )
            row = [0 if i not in relevant_buttons else 1 for i in range(len(self.buttons))]
            equalities.append(row)
            equalities_rhs.append(jolt)

        # Create the LP problem
        prob = LpProblem("Minimize_Sum", LpMinimize)

        n_vars = len(self.buttons)

        # Create variables
        variables = []
        for i in range(n_vars):
            variables.append(
                LpVariable(
                    name=f"x{i}",
                    lowBound=0,
                    upBound=upper_bounds[i],
                    cat='Integer'
                )
            )

        # Objective: minimize sum of all variables
        prob += lpSum(variables)

        # Add equality constraints
        for i, (coefficients, rhs) in enumerate(zip(equalities, equalities_rhs)):
            prob += lpSum([coefficients[j] * variables[j] for j in range(n_vars)]) == rhs, f"Equality_{i}"

        # Solve
        prob.solve(PULP_CBC_CMD(msg=False))

        # Extract results
        obj_value = value(prob.objective)
        if prob.status == 1 and obj_value is not None:
            if isinstance(obj_value, (int, float)):
                return int(obj_value)
        return 0


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
