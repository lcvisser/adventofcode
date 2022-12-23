import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

dataex = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

# Parse data
board, instructions = data.split("\n\n")

# Create the board grid
start = None
grid = []
maxlen = 0
for row in board.split('\n'):
    if row.strip() == "":
        continue
    if start is None:
        startcol = row.index('.')
    start = (0, startcol)
    grid.append(row)
    maxlen = max(maxlen, len(row))

# Pad the grid to make edge calculations easier
for i, row in enumerate(grid):
    grid[i] += ' ' * (maxlen - len(row))

# Parse the commands
distance = 0
commands = []
for c in instructions:
    if c.isdigit():
        distance = 10 * distance + int(c)
    elif c in ('R', 'L'):
        commands.append(("move", distance))
        distance = 0
        commands.append(("rotate", c))
    else:
        # End of command sequence
        if distance != 0:
            commands.append(("move", distance))

# Start moving
orientations = ">V<^"
facing = 0
row, col = start
while commands:
    cmd, arg = commands.pop(0)
    if cmd == "move":
        match facing:
            case 0:  # right
                for _ in range(arg):
                    if col + 1 == len(grid[row]) or grid[row][col + 1] == ' ':
                        # Edge on the right
                        other_edge_first_space = grid[row].find('.')
                        other_edge_first_wall = grid[row].find('#')
                        if other_edge_first_space < other_edge_first_wall:
                            col = other_edge_first_space
                        else:
                            # Wall on the other side, stuck
                            break
                    elif grid[row][col + 1] == '#':
                        # Stuck against wall
                        break
                    else:
                        col = col + 1
            case 2:  # left
                for _ in range(arg):
                    if col - 1 == -1 or grid[row][col - 1] == ' ':
                        # Edge on the left
                        other_edge_first_space = grid[row].rfind('.')
                        other_edge_first_wall = grid[row].rfind('#')
                        if other_edge_first_space > other_edge_first_wall:
                            col = other_edge_first_space
                        else:
                            # Wall on the other side, stuck
                            break
                    elif grid[row][col - 1] == '#':
                        # Stuck against wall
                        break
                    else:
                        col = col - 1
            case 1:  # down
                for _ in range(arg):
                    if row + 1 == len(grid) or (row + 1 < len(grid) and grid[row + 1][col] == ' '):
                        # Edge on the bottom, find where the top of the urrent section is
                        j = row
                        while grid[j][col] in ".#":
                            j -= 1
                            if j == -1:
                                break

                        if grid[j + 1][col] == '.':
                            row = j + 1
                        else:
                            # Stuck against wall
                            break
                    elif grid[row + 1][col] == '#':
                        # Stuck against wall
                        break
                    else:
                        row = row + 1
            case 3:  # up
                for _ in range(arg):
                    if row - 1 == -1 or (row - 1 >= 0 and grid[row - 1][col] == ' '):
                        # Edge on the top, find where the bottom of the current section is
                        j = row
                        while grid[j][col] in ".#":
                            j += 1
                            if j == len(grid):
                                break

                        if grid[j - 1][col] == '.':
                            row = j - 1
                        else:
                            # Stuck against wall
                            break
                    elif grid[row - 1][col] == '#':
                        # Stuck against wall
                        break
                    else:
                        row = row - 1

    elif cmd == "rotate":
        if arg == 'R':
            facing = (facing + 1) % len(orientations)
        else:
            facing = (facing - 1) % len(orientations)

    else:
        pass

# Part 1: find the password
password = 1000 * (row + 1)+ 4 * (col + 1) + facing

print(f"Password: {password}")