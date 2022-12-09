import sys
import math

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# data = """
# R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2
# """

# Parse data
lines = data.strip().split('\n')

# Position x, y for head and tail
posH = [0, 0]
posT = [0, 0]
tail_visited = set()
for line in lines:
    direction, distance = line.split()
    distance = int(distance)

    for i in range(distance):
        # Move head
        # print(f"H={posH}->", end='')
        if direction == 'L':
            posH[0] -= 1
        elif direction == 'R':
            posH[0] += 1
        elif direction == 'U':
            posH[1] += 1
        elif direction == 'D':
            posH[1] -= 1
        # print(f"{posH}")

        # Move tail if needed
        # print(f"T={posT}->", end='')
        distHT = math.dist(posH, posT)
        if 0 <= distHT <= math.sqrt(2):
            # H is less than one block away from T, so nothing to do
            pass
        elif math.sqrt(2) < distHT <= 2:
            # H is 2 blocks away, either exactly horizontally or vertically, let T trail
            if posT[0] == posH[0]:
                posT[1] += int(math.copysign(1, posH[1] - posT[1]))
            elif posT[1] == posH[1]:
                posT[0] += int(math.copysign(1, posH[0] - posT[0]))
            else:
                ValueError("huh?")
        else:
            # Diagonal move to catch up
            posT[0] += int(math.copysign(1, posH[0] - posT[0]))
            posT[1] += int(math.copysign(1, posH[1] - posT[1]))
        # print(f"{posT}")
        # print()

        # Add visited position
        tail_visited.add(str(posT))

# Part 1: number of unique positions visited by tail
print(f"Unique number of places visited by tail: {len(tail_visited)}")
