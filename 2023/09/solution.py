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

extrapolated = []
for h in histories:
    # Compute differences until all zeroes
    diffs = [h, diff(h)]
    while any(diffs[-1]):
        diffs.append(diff(diffs[-1]))

    # Append integrated value
    diffs[-1].append(0)
    for i in reversed(range(1, len(diffs))):
        diffs[i - 1].append(diffs[i - 1][-1] + diffs[i][-1])

    extrapolated.append(diffs[0][-1])

# Part 1: sum of extrapolated values
print(f"Sum of extrapolated values: {sum(extrapolated)}")
