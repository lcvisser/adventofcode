import itertools

# Read data
input_file = "2024/08/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse grid
antennas = {}
height = 0
width = 0
for r, line in enumerate(data.strip().split('\n')):
    height = r
    for c, ch in enumerate(line):
        width = c
        if ch != '.':
            if ch not in antennas.keys():
                antennas[ch] = []

            antennas[ch].append((r, c))

# Find antinodes per antenna frequency
antinodes1 = set()
for antenna_id, antenna_positions in antennas.items():
    for antenna1, antenna2 in itertools.combinations(antenna_positions, 2):
        x1, y1 = antenna1
        x2, y2 = antenna2
        dx = x2 - x1
        dy = y2 - y1

        antinode1 = (x1 - dx, y1 - dy)
        if 0 <= antinode1[0] <= height and 0 <= antinode1[1] <= width:
            antinodes1.add(antinode1)

        antinode2 = (x2 + dx, y2 + dy)
        if 0 <= antinode2[0] <= height and 0 <= antinode2[1] <= width:
            antinodes1.add(antinode2)

# Part 1: number of unique antinodes
print(f"number of unique antinodes: {len(antinodes1)}")

# Find all antinodes per antenna frequency
antinodes2 = set()
for antenna_id, antenna_positions in antennas.items():
    for antenna1, antenna2 in itertools.combinations(antenna_positions, 2):
        # Find all antinodes on the line
        x1, y1 = antenna1
        x2, y2 = antenna2
        dx = x2 - x1
        dy = y2 - y1

        i = 0  # antennas are also antinodes
        while True:
            antinode1 = (x1 - i * dx, y1 - i * dy)
            if 0 <= antinode1[0] <= height and 0 <= antinode1[1] <= width:
                antinodes2.add(antinode1)
                i += 1
            else:
                break

        j = 0  # antennas are also antinodes
        while True:
            antinode2 = (x2 + j * dx, y2 + j * dy)
            if 0 <= antinode2[0] <= height and 0 <= antinode2[1] <= width:
                antinodes2.add(antinode2)
                j += 1
            else:
                break

# Part 2: number of all unique antinodes on the line
print(f"number of all unique antinodes on the line: {len(antinodes2)}")
