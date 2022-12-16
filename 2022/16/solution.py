import sys
import re
import typing

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

data_example = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


class Valve(typing.NamedTuple):
    name: str
    flowrate: int
    connected_to: typing.List


# Parse data
descriptor = re.compile(r"^Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\ ,]+)$")
valves = {}
for line in data.strip().split('\n'):
    p = descriptor.match(line).groups()
    v = Valve(p[0], int(p[1]), list(p[2].split(', ')))
    valves[v.name] = v

# Helper function for a breadth-first search to find the shortest path between two valves
def bfs(src, dst):
    to_visit = [src]
    visited = set()
    visited.add(src)
    parent = {src: None}
    while to_visit:
        v = to_visit.pop(0)

        if v == dst:
            break

        for w in valves[v].connected_to:
            if w not in visited:
                visited.add(w)
                parent[w] = v
                to_visit.append(w)

    d = 0
    if src != dst:
        v = dst
        while parent[v] != None:
            d += 1
            v = parent[v]

    return d

# Determine shortest distance matrix
dist_matrix = {src: {dst: bfs(src, dst) for dst in valves.keys()} for src in valves.keys()}

# Do a depth-first search for all possible paths within 30 minutes
to_visit = [(0, "AA", [], 0)]  # time, current valve, route so far, pressure release so far
max_p = 0
while to_visit:
    t, v, route, p = to_visit.pop(0)

    # Find all reachable (t < 30 min) and useful (flow rate > 0) valves
    possible_dest = [
        (w, dt) for w, dt in dist_matrix[v].items() if w != v and
                                                       w not in route and
                                                       t + dt < 30
                                                       and valves[w].flowrate != 0
    ]

    # Determine if we have somewhere to go still
    if possible_dest:
        for w, dt in possible_dest:
            travel_plus_open_time = dt + 1  # 1 minute to open
            arrival_time = t + travel_plus_open_time
            pressure_release = p + (30 - arrival_time) * valves[w].flowrate
            to_visit.insert(0, (arrival_time, w, route + [w], pressure_release))
    else:
        # End of path; keep track of maximum pressure release
        if p > max_p:
            max_p = p

# Part 1: maximum pressure release
print(f"Maximum pressure release: {max_p}")
