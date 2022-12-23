import sys
import collections
import copy
import functools

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


# Helper functions to see what places in the grid are free
@functools.lru_cache
def check_all_are_free(elf, elves):
    return all(_check_neighbors(elf, elves))


@functools.lru_cache
def check_north(elf, elves):
    nb_state = _check_neighbors(elf, elves)
    if nb_state[0] and nb_state[1] and nb_state[2]:
        r, c = elf
        return True, (r - 1, c)
    else:
        return False, None


@functools.lru_cache
def check_south(elf, elves):
    nb_state = _check_neighbors(elf, elves)
    if nb_state[5] and nb_state[6] and nb_state[7]:
        r, c = elf
        return True, (r + 1, c)
    else:
        return False, None


@functools.lru_cache
def check_west(elf, elves):
    nb_state = _check_neighbors(elf, elves)
    if nb_state[0] and nb_state[3] and nb_state[5]:
        r, c = elf
        return True, (r, c - 1)
    else:
        return False, None


@functools.lru_cache
def check_east(elf, elves):
    nb_state = _check_neighbors(elf, elves)
    if nb_state[2] and nb_state[4] and nb_state[7]:
        r, c = elf
        return True, (r, c + 1)
    else:
        return False, None


@functools.lru_cache
def _check_neighbors(elf, elves):
    r, c = elf
    neighbours = (
        (r - 1, c - 1),  # 0
        (r - 1, c),      # 1
        (r - 1, c + 1),  # 2
        (r,     c - 1),  # 3
        (r,     c + 1),  # 4
        (r + 1, c - 1),  # 5
        (r + 1, c),      # 6
        (r + 1, c + 1)   # 7
    )
    return [p not in elves for p in neighbours]


# Process
def process(elves, check_functions, until=None):
    i = 0
    while True:
        # First half: propose where to move
        dont_move = []
        proposals = {}
        for e in elves:
            if check_all_are_free(e, tuple(elves)):
                dont_move.append(e)
            else:
                for f in check_functions:
                    can_move, new_pos = f(e, tuple(elves))
                    if can_move:
                        proposals[e] = new_pos
                        break
                else:
                    dont_move.append(e)

        num_dont_move = len(dont_move)
        check_functions.rotate(-1)

        # Second half: move
        elves = dont_move
        proposal_counts = collections.Counter(proposals.values())
        for e, p in proposals.items():
            if proposal_counts[p] == 1:
                elves.append(p)
            else:
                elves.append(e)

        # Round finished
        i += 1
        print(f"completed round {i}")

        # Stop if none of the elves moved
        if num_dont_move == len(elves):
            break

        # Stop if we reached the desired round
        if until is not None and i == until:
            break

    return elves, i


# Parse data
elves0 = []
for row, line in enumerate(data.strip().split('\n')):
    for column, p in enumerate(line):
        if p == '#':
            elves0.append((row, column))


# Part 1: compute empty ground after 10 rounds
check_functions = collections.deque([check_north, check_south, check_west, check_east])
elves, _ = process(copy.deepcopy(elves0), check_functions, 10)

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
empty_ground = dimr * dimc - len(elves)
print(f"Empty ground: {empty_ground}")

# Part 2: determine the final round
check_functions = collections.deque([check_north, check_south, check_west, check_east])
elves, round = process(copy.deepcopy(elves0), check_functions)
print(f"Round with no elves moving: {round}")
