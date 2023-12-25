import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
histories = []
for line in data.strip().split('\n'):
    histories.append([int(n) for n in line.split()])


# Extrapolate histories
def diff(h):
    return [h[i + 1] - h[i] for i in range(len(h) - 1)]

extrapolated_forward = []
extrapolated_backwards = []
for h in histories:
    # Compute differences until all zeroes
    diffs = [h, diff(h)]
    while any(diffs[-1]):
        diffs.append(diff(diffs[-1]))

    # Extrapolate forward and backwards
    diffs[-1].append(0)
    diffs[-1].insert(0, 0)
    for i in reversed(range(1, len(diffs))):
        diffs[i - 1].append(diffs[i - 1][-1] + diffs[i][-1])
        diffs[i - 1].insert(0, diffs[i - 1][0] - diffs[i][0])

    extrapolated_forward.append(diffs[0][-1])
    extrapolated_backwards.append(diffs[0][0])

# Part 1: sum of forward extrapolated values
print(f"Sum of forward extrapolated values: {sum(extrapolated_forward)}")

# Part 2: sum of backwards extrapolated values
print(f"Sum of backwards extrapolated values: {sum(extrapolated_backwards)}")
