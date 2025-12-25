#!/usr/bin/env python3
from aoc.utils import run_solution

DAY = 11


def parse_input(data: str) -> dict[str, list[str]]:
    result = {}

    for line in data.splitlines():
        split = line.split(': ')
        result[split[0]] = split[1].split(' ')

    return result


def reverse_graph(graph: dict[str, list[str]], origin: str) -> dict[str, set[str]]:
    stack = [origin]
    visited = set()
    parents = {}
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
            
        children = graph.get(node, [])
        for child in children:
            parents[child] = parents.get(child, set()).union({node})
        visited.add(node)
        stack.extend(children)
    
    return parents

def count_paths(graph: dict[str, list[str]], origin: str, target: str) -> int:
    found = {origin: 1}
    unexplored = reverse_graph(graph, origin)
    
    while unexplored:
        newly_found = set()
        for node in unexplored:
            parents = unexplored[node]
            if all(n in found for n in parents):
                found[node] = sum(map(lambda n: found[n], parents))
                newly_found.add(node)
        for node in newly_found:
            del unexplored[node]
    
    return found.get(target, 0)


def part1(data: str) -> int:
    return count_paths(parse_input(data), 'you', 'out')


def part2(data: str) -> int:
    graph = parse_input(data)

    dac_to_fft = count_paths(graph, 'dac', 'fft')

    if dac_to_fft:
        svr_to_dac = count_paths(graph, 'svr', 'dac')
        fft_to_out = count_paths(graph, 'fft', 'out')
        return svr_to_dac * dac_to_fft * fft_to_out
    else:
        fft_to_dac = count_paths(graph, 'fft', 'dac')
        svr_to_fft = count_paths(graph, 'svr', 'fft')
        dac_to_out = count_paths(graph, 'dac', 'out')
        return svr_to_fft * fft_to_dac * dac_to_out


if __name__ == "__main__":
    run_solution(day=DAY, part1=part1, part2=part2)
