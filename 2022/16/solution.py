import sys
import itertools
import re
import typing

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


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

# Helper function to find all routes through the network and keep track of pressure released
def find_paths(t_end, min_pressure=0):
    # Do a depth-first search for all possible paths within 30 minutes
    route_pressure_release = {}
    to_process = [(0, "AA", 0, [])]  # time, current valve, pressure release so far, visited
    while to_process:
        t, v, p, visited = to_process.pop(0)
        if p > min_pressure:
            route_pressure_release[tuple(visited)] = p

        # Find all reachable in time and useful (flow rate > 0) valves
        possible_dest = [
            (t + dt + 1, w, p + (t_end - (t + dt + 1)) * valves[w].flowrate)
                for w, dt in dist_matrix[v].items() if w != v and
                                                    w not in visited and
                                                    t + dt + 1 < t_end and
                                                    valves[w].flowrate > 0
        ]

        # Go to remaining destinations
        for arrival_time, w, p in possible_dest:
            to_process.insert(0, (arrival_time, w, p, visited + [w]))

    return route_pressure_release

# Part 1: maximum pressure release working alone
pressure_release30 = find_paths(30)
max_p1 = max(pressure_release30.values())
print(f"Maximum pressure release working alone: {max_p1}")

# Part 2: maximum pressure release working with the elephant
pressure_release26 = find_paths(26, max_p1 / 2)  # assume that together we do at least as good of a job as working alone
max_p2 = 0
for my_route, elephant_route in itertools.combinations(pressure_release26.keys(), 2):
    if set(my_route).isdisjoint(set(elephant_route)):
        p = pressure_release26[my_route] + pressure_release26[elephant_route]
        max_p2 = max(max_p2, p)

print(f"Maximum pressure release working together with the elephant: {max_p2}")
