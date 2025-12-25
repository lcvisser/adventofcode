import itertools

with open("2025/09/input.txt") as f:
    data = f.read()

tiles = []
for row in data.strip().split("\n"):
    x, y = [int(v) for v in row.split(",")]
    tiles.append((x, y))

largest_area = 0
for first, second in itertools.combinations(tiles, 2):
    x1, y1 = first
    x2, y2 = second
    area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
    if area > largest_area:
        largest_area = area

print(f"Largest rectangle area: {largest_area}")
