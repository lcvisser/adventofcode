import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
grid = []
start = None
for r, line in enumerate(data.strip().split('\n')):
    if 'S' in line:
        assert start is None
        c = line.index('S')
        start = (r, c)

    grid.append(line)

# Determine connected pipes
connected = []
r, c = start
if r != 0 and grid[r - 1][c] in "|7F":
    connected.append((r - 1, c))
if r != len(grid) and grid[r + 1][c] in "|JL":
    connected.append((r + 1, c))
if c != 0 and grid[r][c - 1] in "-LF":
    connected.append((r, c - 1))
if c != len(grid[0]) - 1 and grid[r][c + 1] in "-J7":
    connected.append((r, c + 1))

# Start towards one of the two connected pipes and travel until reaching the start again
path = [start, connected[0]]
while path[-1] != start:
    r, c = path[-1]
    match grid[r][c]:
        case '|':
            to_check = [(r - 1, c), (r + 1, c)]
        case '-':
            to_check = [(r, c - 1), (r, c + 1)]
        case 'L':
            to_check = [(r - 1, c), (r, c + 1)]
        case 'J':
            to_check = [(r - 1, c), (r, c - 1)]
        case '7':
            to_check = [(r, c - 1), (r + 1, c)]
        case 'F':
            to_check = [(r, c + 1), (r + 1, c)]

    # Make sure not to go back
    if to_check[0] != path[-2]:
        path.append(to_check[0])
    else:
        path.append(to_check[1])

# Part 1: furthest distance from start
dist = (len(path) - 1) // 2
print(f"Furthest distance: {dist}")
