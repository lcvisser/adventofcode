import sys
import functools

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
jets = tuple(1 if j == '>' else -1 for j in data.strip())
num_jets = len(jets)

# Rocks, defined bottom to top
rocks = (
    (0xF << 1, ),  # -
    (0x2 << 2, 0x7 << 2, 0x2 << 2),  # +
    (0x7 << 2, 0x1 << 2, 0x1 << 2),  # mirrored L
    (0x1 << 4, 0x1 << 4, 0x1 << 4, 0x1 << 4),  # |
    (0x3 << 3, 0x3 << 3)  # 2x2 cube
)
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
    # Initialize
    jet_index = 0
    rock_index = 0

    # Cave as a stack, growing on the right as we go up
    cave = [0x7f]

    # Keep a cache of cave/rock/jet comboinations to see if we're repeating
    seen_combinations = {}
    extra_heigth = 0
    cycle_found = False

    # Start dropping rocks
    rock_count = 0
    while rock_count < target_rock_count:
        # Determine the maximum fill for each column to see what we should save; if the whole width is filled, we know
        # (almost for sure) that the cave won't change below
        found = 0
        h = len(cave)
        depth = 0
        while found != 0x7f and h > 0:
            h -= 1
            depth += 1
            found = found | cave[h]

        # Determien if we are repeating
        if not cycle_found:
            combination = (tuple(cave[-depth:]), rock_index, jet_index)
            if combination in seen_combinations.keys():
                # Determine repeate cycle parameters
                cycle_offset = list(seen_combinations.keys()).index(combination)
                cycle_length = len(seen_combinations.keys()) - cycle_offset
                cycle_growth = len(cave) - 1 - seen_combinations[combination]
                extra_cycles = (target_rock_count - rock_count) // cycle_length

                # Fast-forward
                extra_heigth = cycle_growth * extra_cycles
                rock_count += extra_cycles * cycle_length
                cycle_found = True
            else:
                seen_combinations[combination] = len(cave) - 1

        # Get rock
        rock = rocks[rock_index]

        # Add rows for the rock and empty space
        rock_size = len(rock)
        for _ in range(rock_size + 3):
            cave.append(0)

        # Go down the cave, pushing the rock before every step
        for i in reversed(range(1, len(cave) - rock_size + 1)):
            jet_push = jets[jet_index]
            jet_index = (jet_index + 1) % num_jets

            cave_section = tuple(cave[i - 1:i + rock_size])
            rock, stopped, section_update = step(jet_push, rock, cave_section)

            # "Draw" the rock only when it has stopped
            if stopped:
                for x, r in enumerate(section_update):
                    cave[i + x] = r

                break

        # Remove the empty layers of cave
        while cave[-1] == 0:
            cave.pop()

        # Next rock
        rock_count += 1
        rock_index = (rock_index + 1) % num_rocks

    # Total height minus the floor
    return len(cave) - 1 + extra_heigth

# Part 1: drop 2022 rocks
h = drop(2022)
print(f"Rock height after 2022 rocks: {h}")

# Part 2: drop a lot of rocks
desired_rock_count = 1000000000000
h = drop(desired_rock_count)
print(f"Rock height after {desired_rock_count} rocks: {h}")
