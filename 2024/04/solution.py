# Read data
input_file = "2024/04/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
grid = []
for line in data.strip().split('\n'):
    grid.append(line)

max_rows = len(grid)
max_cols = len(grid[0])

# Row and column increments for each direction
DIRECTIONS = {
    "up": (-1, 0),
    "up-right": (-1, 1),
    "right": (0, 1),
    "down-right": (1, 1),
    "down": (1, 0),
    "down-left": (1, -1),
    "left": (0, -1),
    "up-left": (-1, -1)
}

# Helper functions
def letter_at(r, c):
    if r < 0 or r >= max_rows:
        return None
    elif c < 0 or c >= max_cols:
        return None
    else:
        return grid[r][c]


def has_xmas_in_direction(r, c, direction):
    dr, dc = DIRECTIONS[direction]
    return all(letter_at(r + i * dr, c + i * dc) == q for i, q in enumerate("XMAS"))


# Traverse the grid and count
total_xmas_count = 0
for r, row in enumerate(grid):
    for c, letter in enumerate(row):
        if letter == 'X':
            for dir in DIRECTIONS.keys():
                if has_xmas_in_direction(r, c, dir):
                    total_xmas_count += 1

# Part 1: total number of times XMAS appears
print(f"Total number of times XMAS appears: {total_xmas_count}")
