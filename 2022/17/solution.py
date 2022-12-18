import sys
import collections

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


def drop(target_rock_count):
    # Cave as a stack, growing on the right as we go up
    cave = collections.deque([0x7f])

    rock_count = 0
    while rock_count < target_rock_count:
        # Get rock
        rock = list(rocks[0])
        rocks.rotate(-1)

        # Add rows for the rock and empty space
        rock_size = len(rock)
        for _ in range(rock_size + 3):
            cave.append(0)

        for i in reversed(range(1, len(cave) - rock_size + 1)):
            jet_push = jets[0]
            jets.rotate(-1)

            # Check collision with wall or other rocks
            for x, r in enumerate(rock):
                lb = 0x80 | cave[i + x]
                rb = cave[i + x]
                pushed_r = push(r, jet_push)
                blocked_left = (pushed_r & lb > 0) and jet_push == -1
                blocked_right = (pushed_r & rb > 0 or r & 0x1) and jet_push == 1
                if blocked_left or blocked_right:
                    break
            else:
                rock = [push(r, jet_push) for r in rock]

            # Check if we hit the bottom
            if any(r & cave[i + x - 1] for x, r in enumerate(rock)):
                for x, r in enumerate(rock):
                    cave[i + x] = cave[i + x] | r

                break

        # Remove the empty layers of cave
        while cave[-1] == 0:
            cave.pop()

        if cave[-1] == 127:
            print(rock_count)

        rock_count += 1

    return len(cave) - 1

# Part 1: drop 2022 rocks
h = drop(2022)
print(f"Rock height after 2022 rocks: {h}")

# Part 2: drop a lot of rocks
desired_rock_count = 1000000000000
min_cycle = num_jets * num_rocks
drop(1000000000000)

# 1514285714288 <--
# 1514285714287
