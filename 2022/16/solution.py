import sys
import itertools
import re
import typing

# Read data
#input_file = sys.argv[1]
#with open(input_file) as f:
#    data = f.read()

data = """
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
t_end = 30
max_p1 = 0
to_process = [(0, "AA", 0, [])]  # time, current valve, pressure release so faf, visited
while to_process:
    t, v, p, visited = to_process.pop(0)

    # Keep track of maximum pressure release
    max_p1 = max(max_p1, p)

    # Find all reachable (t < 30 min) and useful (flow rate > 0) valves
    possible_dest = [
        (t + dt + 1, w, p + (t_end - (t + dt + 1)) * valves[w].flowrate)
            for w, dt in dist_matrix[v].items() if w != v and
                                                   w not in visited and
                                                   t + dt + 1 < t_end and
                                                   valves[w].flowrate > 0
    ]

    # Go to remaning destinations
    for arrival_time, w, p in possible_dest:
        to_process.insert(0, (arrival_time, w, p, visited + [v]))

# Part 1: maximum pressure release working alone
print(f"Maximum pressure release working alone: {max_p1}")

# Do a depth-first search for all possible combinations of visits within 26 minutes
t_end = 26
max_p2 = 0
to_process = [((0, "AA", 0), (0, "AA", 0), [])]  # time, current valve and pressure release for me and elephant; visited
while to_process:
    me, elephant, visited = to_process.pop(0)
    mt, mloc, mp = me
    et, eloc, ep = elephant

    # Keep track of maximum pressure release
    max_p2 = max(max_p2, mp + ep)

    # Find all reachable (t < 26 min) and useful (flow rate > 0) valves for me
    my_possible_dest = [
        (mt + dt + 1, v, mp + (t_end - (mt + dt + 1)) * valves[v].flowrate)
            for v, dt in dist_matrix[mloc].items() if v != mloc and
                                                      v not in visited and
                                                      mt + dt + 1 < t_end and
                                                      valves[v].flowrate > 0
    ]

    # Find all reachable (t < 26 min) and useful (flow rate > 0) valves for the elephant
    elephant_possible_dest = [
        (et + dt + 1, w, ep + (t_end - (et + dt + 1)) * valves[w].flowrate)
            for w, dt in dist_matrix[eloc].items() if w != eloc and
                                                      w not in visited and
                                                      et + dt + 1 < t_end and
                                                      valves[w].flowrate > 0
    ]

    # Go to remaining destinations (all combinations thereof)
    for d1, d2 in itertools.product(my_possible_dest, elephant_possible_dest):
        if d1[1] != d2[1]:  # don't go to the same valve
            to_process.insert(0, (d1, d2, visited + [d1[1], d2[1]]))

# Part 2: maximum pressure release working with the elephant
print(f"Maximum pressure release working together with the elephant: {max_p2}")
