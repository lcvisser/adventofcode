import sys
import collections
import functools
import math

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
valley_description = data.strip().split('\n')
height = len(valley_description)
width = len(valley_description[0])


class Blizzard:
    def __init__(self, init_row, init_col, direction, dim):
        self.init_row = init_row
        self.init_col = init_col
        self.direction = direction
        self.dim = dim

    def position(self, t):
        # Assume no blizzards will end up in the entrance or exit locations
        match self.direction:
            case '>':
                row = self.init_row
                col = 1 + (self.init_col - 1 + t) % (self.dim - 2)
            case '<':
                row = self.init_row
                col = 1 + (self.init_col - 1 - t) % (self.dim - 2)
            case 'v':
                row = 1 + (self.init_row - 1 + t) % (self.dim - 2)
                col = self.init_col
            case '^':
                row = 1 + (self.init_row - 1 - t) % (self.dim - 2)
                col = self.init_col

        return row, col


blizzards = []
for r in range(height):
    for c in range(width):
        direction = valley_description[r][c]
        if direction in ('>', '<'):
            blizzards.append(Blizzard(r, c, direction, width))
        elif direction in ('v', '^'):
            blizzards.append(Blizzard(r, c, direction, height))
        else:
            pass

# Blizzard pattern repeats
blizzard_cycle_time = (height - 2) * (width - 2) // math.gcd(height - 2, width - 2)

# Position is (row, col)
start = (0, valley_description[0].index('.'))
dest = (height - 1, valley_description[height - 1].index('.'))


# Helper function to compute all blizzards at time t
@functools.cache
def get_blizzard_positions(t):
    return {b.position(t) for b in blizzards}


# Helper functions to get all valid non-blizzard neighbor positions from given position
@functools.cache
def get_neighbors(t, pos):
    r, c = pos
    possible_neighbors = [pos]  # waiting in place is an option too and can be faster!
    if pos == start:
        possible_neighbors.append((r + 1, c))
    elif pos == dest:
        possible_neighbors.append((r - 1, c))
    else:
        if r > 1:
            possible_neighbors.append((r - 1, c))
        if r < height - 2:
            possible_neighbors.append((r + 1, c))
        if c > 1:
            possible_neighbors.append((r, c - 1))
        if c < width - 2:
            possible_neighbors.append((r, c + 1))

    if pos == (dest[0] - 1, dest[1]):
        possible_neighbors.append(dest)

    if pos == (start[0] + 1, start[1]):
        possible_neighbors.append(start)

    blizzard_positions = get_blizzard_positions(t)
    allowed_neighbors = [p for p in possible_neighbors if p not in blizzard_positions]

    return allowed_neighbors


# Breadth-first search to find shortest route
def find_path(begin, end, t0=0):
    travel_time = float("inf")
    state = (t0, begin, [begin])
    visited = {(t0 % blizzard_cycle_time, begin)}

    to_process = collections.deque()
    to_process.append(state)
    while to_process:
        t, v, route = to_process.popleft()
        if v == end:
            travel_time = t - t0
            break

        # Get state of the map considering cyclic nature of the blizzards
        options = get_neighbors((t + 1) % blizzard_cycle_time, v)
        for w in options:
            if ((t + 1) % blizzard_cycle_time, w) not in visited:
                # State is cyclic, but track actual time
                visited.add(((t + 1) % blizzard_cycle_time, w))
                to_process.append((t + 1, w, route + [w]))

    return travel_time

# Part 1: find the shortest travel time
t1 = find_path(start, dest)
print(f"Shortest travel time: {t1}")

# Part 2: go back for the snacks
t2 = find_path(dest, start, t0=t1)
t3 = find_path(start, dest, t0=t1 + t2)
print(f"Time to reach goal, go back, and go to goal again: {t1 + t2 + t3}")
