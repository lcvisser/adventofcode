import itertools
import sys


# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
grid = data.strip().split('\n')
def get_adjacent_cell(r, c):
    if r < 0 or r >= len(grid):
        return '.'
    elif c < 0 or c >= len(grid[0]):
        return '.'
    else:
        return grid[r][c]

# Find part numbers
part_numbers = []
for r, line in enumerate(grid):
    current_number = ""
    is_part_number = False
    for c, x in enumerate(line):
        if x in "0123456789":
            current_number += x
            for dr, dc in itertools.product([-1, 0, 1], repeat=2):
                if get_adjacent_cell(r + dr, c + dc) not in ".0123456789":
                    is_part_number = True

            if c == len(line) - 1 and is_part_number:
                part_numbers.append(int(current_number))
        else:
            if is_part_number:
                part_numbers.append(int(current_number))

            current_number = ""
            is_part_number = False

# Part 1: sum of part numbers
print(f"Sum of part numbers: {sum(part_numbers)}")
