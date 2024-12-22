import functools

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
        available_towels = tuple(x.strip() for x in line.split(','))
    else:
        desired_towels.append(line.strip())


# Memoized recursive depth-first search, because the individual towels in the in-progress towel are indistinguishable
@functools.cache
def make_towel(desired, current, available):
    num_solutions = 0
    if current == desired:
        return 1
    else:
        for p in filter(lambda x: desired.startswith(current + x), available):
            num_solutions += make_towel(desired, current + p, available)

    return num_solutions


# Check designs
possible = 0
num_patterns = 0
for t in desired_towels:
    if (n := make_towel(t, "", available_towels)) > 0:
        possible += 1
        num_patterns += n

# Part 1: number of possible designs
print(f"Number of possible designs: {possible}")

# Part 2: sum of possible design options
print(f"Sum of number of possible patterns: {num_patterns}")
