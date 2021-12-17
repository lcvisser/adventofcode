import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
fish = [int(x) for x in data.strip().split(',')]

# Simulate
for i in range(80):
    new_fish = 0
    for j in range(len(fish)):
        if fish[j] == 0:
            fish[j] = 6
            new_fish += 1
        else:
            fish[j] -= 1

    fish.extend([8] * new_fish)

# Part 1
print("Number of fish: {}".format(len(fish)))
