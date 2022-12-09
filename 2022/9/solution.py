import sys
import math

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')


def follow(posH, posT):
    # Move tail if needed
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
        # Diagonal move to catch up
        posT[0] += int(math.copysign(1, posH[0] - posT[0]))
        posT[1] += int(math.copysign(1, posH[1] - posT[1]))

    return posT


def process(lines, N_knots):
    # Position x, y for each knot
    knots = [[0, 0] for _ in range(N_knots)]
    tail_visited = set()

    for line in lines:
        direction, distance = line.split()
        distance = int(distance)

        for i in range(distance):
            # Move head
            if direction == 'L':
                knots[0][0] -= 1
            elif direction == 'R':
                knots[0][0] += 1
            elif direction == 'U':
                knots[0][1] += 1
            elif direction == 'D':
                knots[0][1] -= 1

            # Move other knots
            for i in range(1, N_knots):
                knots[i] = follow(knots[i - 1], knots[i])

            # Add visited tail position
            tail_visited.add(str(knots[-1]))

    return len(tail_visited)


# Part 1: number of unique positions visited by tail
print(f"Unique number of places visited by tail: {process(lines, 2)}")

# Part 2: number of unique positions visited by 10th knot
print(f"Unique number of places visited by tail: {process(lines, 10)}")
