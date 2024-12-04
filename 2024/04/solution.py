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


def has_word_in_direction(r, c, direction, word):
    dr, dc = DIRECTIONS[direction]
    return all(letter_at(r + i * dr, c + i * dc) == q for i, q in enumerate(word))


def has_xmas_in_direction(r, c, direction):
    return has_word_in_direction(r, c, direction, "XMAS")


# Traverse the grid and count
total_xmas_count1 = 0
for r, row in enumerate(grid):
    for c, letter in enumerate(row):
        if letter == 'X':
            for dir in DIRECTIONS.keys():
                if has_xmas_in_direction(r, c, dir):
                    total_xmas_count1 += 1

# Part 1: total number of times XMAS appears
print(f"Total number of times XMAS appears: {total_xmas_count1}")


def has_mas_in_direction(r, c, direction):
    return has_word_in_direction(r, c, direction, "MAS")


def has_xmas_at(r, c):
    return [
        has_mas_in_direction(r, c, "down-right") and has_mas_in_direction(r + 2, c, "up-right"),  # variant 1
        has_mas_in_direction(r, c, "down-right") and has_mas_in_direction(r, c + 2, "down-left"),  # variant 2
        has_mas_in_direction(r, c, "up-right") and has_mas_in_direction(r, c + 2, "up-left"),  # variant 3
        has_mas_in_direction(r, c, "down-left") and has_mas_in_direction(r + 2, c, "up-left")  # variant 4
    ]

# Traverse the grid and count
total_xmas_count2 = 0
for r, row in enumerate(grid):
    for c, letter in enumerate(row):
        if letter == 'M':
            xmas_at = has_xmas_at(r, c)
            if any(xmas_at):
                # An 'M' can be part of multiple X-MAS!
                total_xmas_count2 += xmas_at.count(True)


# Part 2: total number of times X-MAS appears
print(f"Total number of times X-MAS appears: {total_xmas_count2}")
