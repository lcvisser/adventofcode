# Read data
input_file = "2024/19/input.txt"
with open(input_file) as f:
    data = f.read()

# Parse data
available_towels = []
desired_towels = []
sep = False
for line in data.strip().split('\n'):
    if line == "":
        sep = True
        continue

    if not sep:
        available_towels = [x.strip() for x in line.split(',')]
    else:
        desired_towels.append(line.strip())


# Depth first search for a possible combination
def make_towel(desired, available):
    is_possible = False

    to_check = list(filter(lambda x: desired.startswith(x), available))
    while to_check:
        towel = to_check.pop(0)
        if towel == desired:
            is_possible = True
            break

        possible = list(filter(lambda x: desired.startswith(towel + x), available))
        for p in possible:
            to_check.insert(0, towel + p)

    return is_possible

# Check designs
possible = 0
for t in desired_towels:
    if make_towel(t, available_towels):
        possible += 1

# Part 1: number of possible designs
print(f"Number of possible designs: {possible}")
