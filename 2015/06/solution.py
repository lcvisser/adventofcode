import re

with open("2015/06/input.txt") as f:
    data = f.read()

grid = []
for _ in range(1000):
    grid.append([False] * 1000)

COORDINATE = re.compile(r"([0-9]+,[0-9]+)")

for instruction in data.strip().split("\n"):
    corners = COORDINATE.findall(instruction)
    assert len(corners) == 2
    first, second = corners
    x1, y1 = [int(v) for v in first.split(",")]
    x2, y2 = [int(v) for v in second.split(",")]

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if instruction.startswith("turn on"):
                grid[x][y] = True
            elif instruction.startswith("toggle"):
                grid[x][y] = not grid[x][y]
            elif instruction.startswith("turn off"):
                grid[x][y] = False
            else:
                raise RuntimeError(instruction)

num_lights_on = 0
for row in grid:
    for c in row:
        if c:
            num_lights_on += 1

# Part 1
print(f"Number of lights on: {num_lights_on}")
