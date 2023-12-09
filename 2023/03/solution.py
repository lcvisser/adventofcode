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
gears = {}
for r, line in enumerate(grid):
    current_number = ""
    is_part_number = False
    is_gear = False
    gear_location = None
    for c, x in enumerate(line):
        if x in "0123456789":
            current_number += x
            for dr, dc in itertools.product([-1, 0, 1], repeat=2):
                y = get_adjacent_cell(r + dr, c + dc)
                if y not in ".0123456789":
                    is_part_number = True
                if y == '*':
                    is_gear = True
                    gear_location = (r + dr, c + dc)
                    if gear_location not in gears.keys():
                        gears[gear_location] = []

            if c == len(line) - 1 and is_part_number:
                part_numbers.append(int(current_number))
                if is_gear:
                    gears[gear_location].append(int(current_number))
        else:
            if is_part_number:
                part_numbers.append(int(current_number))
                if is_gear:
                    gears[gear_location].append(int(current_number))

            current_number = ""
            is_part_number = False
            is_gear = None
            gear_location = None

# Part 1: sum of part numbers
print(f"Sum of part numbers: {sum(part_numbers)}")

# Part 2: sum of gear ratios
sum_of_gear_ratios = sum([g[0] * g[1] for g in gears.values() if len(g) == 2])
print(f"Sum of gear ratios: {sum_of_gear_ratios}")
