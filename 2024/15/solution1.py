# Read data
input_file = "2024/15/input.txt"
with open(input_file) as f:
    data = f.read()

EMPTY = '.'
WALL = '#'
ROBOT = '@'
BOX = 'O'
DIRECTIONS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

# Grid properties
grid = []
height = 0
width = 0

# Robot
robot = [0, 0]
instructions = []

# Parse data
parsing_grid = True
parsing_instructions = False
for r, row in enumerate(data.strip().split('\n')):
    if parsing_grid:
        height = r
        grid_row = []
        for c, ch in enumerate(row):
            width = c
            if ch == ROBOT:
                robot = (r, c)

            grid_row.append(ch)
        grid.append(grid_row)
    elif parsing_instructions:
        for ch in row:
            instructions.append(ch)

    if row.strip() == "":
        parsing_grid = False
        parsing_instructions = True


# Helper functions
def print_grid(g):
    for row in g:
        print(''.join('.' if x == 0 else str(x) for x in row))
    print()


def object_at(x, y):
    return grid[x][y]


def object_can_move(x, y, d):
    dx, dy = DIRECTIONS[d]
    o = object_at(x + dx, y + dy)
    if o == EMPTY:
        can_move = True
    elif o == WALL:
        can_move = False
    elif o == BOX:
        can_move = object_can_move(x + dx, y + dy, d)
    else:
        raise ValueError

    return can_move


def move_object(x, y, d, o):
    if not object_can_move(x, y, d):
        return x, y

    dx, dy = DIRECTIONS[d]
    if grid[x + dx][y + dy] == BOX:
        move_object(x + dx, y + dy, d, BOX)

    grid[x][y] = EMPTY
    grid[x + dx][y + dy] = o

    return x + dx, y + dy


# Process instructions
while instructions:
    direction = instructions.pop(0)
    robot = move_object(*robot, direction, ROBOT)

# Compute coordinates
sum_of_coordinates = 0
for r, row in enumerate(grid):
    for c, ch in enumerate(row):
        if ch == BOX:
            sum_of_coordinates += 100 * r + c

# Part 1: sum of coordinates
print(f"Sum of coordinates: {sum_of_coordinates}")
