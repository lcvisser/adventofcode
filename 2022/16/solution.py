import sys
import dataclasses
import heapq
import typing
import re

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

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


@dataclasses.dataclass
class Valve:
    name: str
    rate: int
    connected_to: typing.List

    def __init__(self, name, rate, connected_to):
        self.name = name
        self.rate = rate
        self.connected_to = connected_to
        self.open = False


descriptor = re.compile(r"^Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\ ,]+)$")

valves = {}
for line in data.strip().split('\n'):
    p = descriptor.match(line).groups()
    v = Valve(p[0], int(p[1]), list(p[2].split(', ')))
    valves[v.name] = v
    print(v)


# Breadth-first search to find shortest path
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

dist_matrix = {src: {dst: bfs(src, dst) for dst in valves.keys()} for src in valves.keys()}
for r, v in dist_matrix.items():
    print(r, v)

curr = "AA"
total_pressure_release = 0
t = 0
t_end = 30
while t <= t_end:
    print(t, curr)
    options_release = []
    for v in valves.values():
        if v.open:
            continue

        time_to_get_there = dist_matrix[curr][v.name] + 1  # plus one minute to open the valve
        if time_to_get_there > t_end - t:
            continue

        p = (t_end - t - time_to_get_there) * valves[v.name].rate
        options_release.append((p, v.name, time_to_get_there))

    if options_release:
        dp, v, dt = max(options_release, key=lambda x: x[0])
        valves[v].open = True
        total_pressure_release += dp
        t += dt
        curr = v
    else:
        t += 1

print(total_pressure_release)