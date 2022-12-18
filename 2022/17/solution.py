import sys
import collections
import functools

# Read data
# input_file = sys.argv[1]
# with open(input_file) as f:
#     data = f.read()

data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

# Parse data
jets = collections.deque(1 if j == '>' else -1 for j in data.strip())
num_jets = len(jets)

# Rocks, defined bottom to top
rocks = collections.deque([
    (0xF << 1, ),  # -
    (0x2 << 2, 0x7 << 2, 0x2 << 2),  # +
    (0x7 << 2, 0x1 << 2, 0x1 << 2),  # mirrored L
    (0x1 << 4, 0x1 << 4, 0x1 << 4, 0x1 << 4),  # |
    (0x3 << 3, 0x3 << 3)  # 2x2 cube
])
num_rocks = len(rocks)


# Helper function to push a rock left or right
def push(r, j):
    if j > 0:
        return r >> j
    else:
        return r << abs(j)


@functools.cache
def step(jet_push, rock, cave_section):
    # Check collision with wall or other rocks
    for x, r in enumerate(rock):
        lb = 0x80 | cave_section[1 + x]
        rb = cave_section[1 + x]
        pushed_r = push(r, jet_push)
        blocked_left = (pushed_r & lb > 0) and jet_push == -1
        blocked_right = (pushed_r & rb > 0 or r & 0x1) and jet_push == 1
        if blocked_left or blocked_right:
            break
    else:
        rock = tuple(push(r, jet_push) for r in rock)

    # Check if we hit anywhere on the row below
    if any(r & cave_section[x] for x, r in enumerate(rock)):
        section_update = tuple(cave_section[1 + x] | r for x, r in enumerate(rock))
        stopped = True
    else:
        section_update = None
        stopped = False

    return rock, stopped, section_update


def drop(target_rock_count):
    # Cave as a stack, growing on the right as we go up
    cave = [0x7f]

    rock_count = 0
    while rock_count < target_rock_count:
        # Get rock
        rock = rocks[0]
        rocks.rotate(-1)

        # Add rows for the rock and empty space
        rock_size = len(rock)
        for _ in range(rock_size + 3):
            cave.append(0)

        for i in reversed(range(1, len(cave) - rock_size + 1)):
            jet_push = jets[0]
            jets.rotate(-1)

            cave_section = tuple(cave[i - 1:i + rock_size])
            rock, stopped, section_update = step(jet_push, rock, cave_section)
            if stopped:
                for x, r in enumerate(section_update):
                    cave[i + x] = r

                break

        # Remove the empty layers of cave
        while cave[-1] == 0:
            cave.pop()

        rock_count += 1

    return len(cave) - 1

# Part 1: drop 2022 rocks
h = drop(2022)
print(f"Rock height after 2022 rocks: {h}")
step.cache_clear()

# Part 2: drop a lot of rocks
desired_rock_count = 1000000000000
min_cycle = 241 * num_jets * num_rocks
full_cycles, partial_cycles = divmod(desired_rock_count, min_cycle)
h = drop(min_cycle) * full_cycles + drop(partial_cycles)
print(h)
print(step.cache_info())
# 1514285714288 <--
# 1514285714287
# 1399970062786