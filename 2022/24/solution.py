import sys
import collections
import functools

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

dataex = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""


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


# Position is (row, col)
start = (0, valley_description[0].index('.'))
dest = (height - 1, valley_description[height - 1].index('.'))


@functools.cache
def get_blizzard_positions(t):
    return {b.position(t) for b in blizzards}


@functools.cache
def get_neighbors(t, pos):
    r, c = pos
    possible_neighbors = []
    if pos == start:
        possible_neighbors.append((r + 1, c))
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

    blizzard_positions = get_blizzard_positions(t)
    allowed_neighbors = [p for p in possible_neighbors if p not in blizzard_positions]
    if not allowed_neighbors:
        allowed_neighbors = None

    return allowed_neighbors


# Breadth-first search to find shortest route to exit
to_process = collections.deque()
state = (0, start, [start])
to_process.append(state)
visited = {(0, start)}
while to_process:
    t, v, route = to_process.popleft()
    if v == dest:
        print(f"Reached {v} == {dest} at t={t}")
        break

    options = get_neighbors(t + 1, v)
    if options is None:
        # Nowhere to go, wait
        to_process.append((t + 1, v, route + [v]))
    else:
        for w in options:
            if (t + 1, w) not in visited:
                visited.add((t + 1, w))
                to_process.append((t + 1, w, route + [w]))


# 267 is too low
# 268 is too low