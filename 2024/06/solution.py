# Read data
input_file = "2024/06/input.txt"
with open(input_file) as f:
    data = f.read()


# Row and column increments for each direction
DIRECTIONS = {
    "up": (-1, 0),
    "right": (0, 1),
    "down": (1, 0),
    "left": (0, -1),
}


# Parse grid
start = None
obstacles = []
width = 0
height = 0
for r, line in enumerate(data.strip().split('\n')):
    height = r
    for c, char in enumerate(line):
        width = c
        if char == '^':
            start = (r,c)
        elif char == '#':
            obstacles.append((r, c))


# Keep track of unique visited positiions
visited = set()
visited.add(start)

# Go
x, y = start
direction = "up"
while True:
    dx, dy = DIRECTIONS[direction]
    if (x + dx, y + dy) in obstacles:
        idx = list(DIRECTIONS.keys()).index(direction)
        idx = (idx + 1) % 4
        direction = list(DIRECTIONS.keys())[idx]
    else:
        x, y = x + dx, y + dy

    if x < 0 or x > width or y < 0 or y > height:
        break
    else:
        visited.add((x, y))

# Part 1: number of positions visited
print(f"Number of positions visited: {len(visited)}")
