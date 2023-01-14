import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Part 1: simple instructions
position = 0
depth = 0
for instruction in data.split('\n'):
    # Skip possible empty lines
    if not instruction.strip():
        continue

    # Parse instructions
    direction, distance = instruction.split(' ')
    distance = int(distance)

    # Increment position/depth
    if direction == "forward":
        position += distance
    elif direction == "down":
        depth += distance
    elif direction == "up":
        depth -= distance
    else:
        print(f"Unknown instruction: `{instruction}`")

# Answer
print("position={}, depth={}, answer={}".format(position, depth, position * depth))

# Part 2: aiming
position = 0
depth = 0
aim = 0
for instruction in data.split('\n'):
    # Skip possible empty lines
    if not instruction.strip():
        continue

    # Parse instructions
    direction, distance = instruction.split(' ')
    distance = int(distance)

    # Increment position/depth
    if direction == "forward":
        position += distance
        depth += distance * aim
    elif direction == "down":
        aim += distance
    elif direction == "up":
        aim -= distance
    else:
        print(f"Unknown instruction: `{instruction}`")

# Answer
print("position={}, depth={}, answer={}".format(position, depth, position * depth))
