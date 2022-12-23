import sys
import collections
import functools

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

data2 = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""

data1 = """
.....
..##.
..#..
.....
..##.
.....
"""

# Parse data
elves = []
for row, line in enumerate(data.strip().split('\n')):
    for column, p in enumerate(line):
        if p == '#':
            elves.append((row, column))


# Helper functions to see what places in the grid are free
def check_all_are_free(elf, elves):
    r, c = elf
    neighbours = (
        (r - 1, c - 1),
        (r - 1, c),
        (r - 1, c + 1),
        (r, c - 1),
        (r, c + 1),
        (r + 1, c - 1),
        (r + 1, c),
        (r + 1, c + 1)
    )
    return _all_are_free(neighbours, elves)

def check_north(elf, elves):
    r, c = elf
    neighbours = (
        (r - 1, c - 1),
        (r - 1, c),
        (r - 1, c + 1)
    )
    if _all_are_free(neighbours, elves):
        return True, (r - 1, c)
    else:
        return False, None

def check_south(elf, elves):
    r, c = elf
    neighbours = (
        (r + 1, c - 1),
        (r + 1, c),
        (r + 1, c + 1)
    )
    if _all_are_free(neighbours, elves):
        return True, (r + 1, c)
    else:
        return False, None

def check_west(elf, elves):
    r, c = elf
    neighbours = (
        (r - 1, c - 1),
        (r, c - 1),
        (r + 1, c - 1),
    )
    if _all_are_free(neighbours, elves):
        return True, (r, c - 1)
    else:
        return False, None

def check_east(elf, elves):
    r, c = elf
    neighbours = (
        (r - 1, c + 1),
        (r, c + 1),
        (r + 1, c + 1)
    )
    if _all_are_free(neighbours, elves):
        return True, (r, c + 1)
    else:
        return False, None

def _all_are_free(neighbours, elves):
    return all(tuple(_is_free(nb, tuple(elves)) for nb in neighbours))

@functools.cache
def _is_free(pos, elves):
    return pos not in elves


# List of check functions, in order
check_functions = collections.deque([check_north, check_south, check_west, check_east])

# Process
num = len(elves)
i = 0
while i < 10:
    dont_move = []
    proposals = {}
    # First half: propose where to move
    for e in elves:
        if check_all_are_free(e, elves):
            dont_move.append(e)
        else:
            for f in check_functions:
                can_move, new_pos = f(e, elves)
                if can_move:
                    proposals[e] = new_pos
                    break
            else:
                dont_move.append(e)

    check_functions.rotate(-1)

    # Second half: move
    elves = dont_move.copy()
    proposal_counts = collections.Counter(proposals.values())
    for e, p in proposals.items():
        if proposal_counts[p] == 1:
            elves.append(p)
        else:
            elves.append(e)

    if len(dont_move) == num:
        break

    assert len(elves) == num, f"{len(elves)}, {num}"
    i += 1

# Determine the rectangle size
minr = minc = 1000000000000
maxr = maxc = 0
for r, c in elves:
    minr = min(minr, r)
    maxr = max(maxr, r)
    minc = min(minc, c)
    maxc = max(maxc, c)

dimr = maxr - minr + 1
dimc = maxc - minc + 1

# Part 1: compute empty ground after 10 rounds
empty_ground = dimr * dimc - num
print(f"Empty_ground: {empty_ground}")
