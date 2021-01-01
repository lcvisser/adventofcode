import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

adapters = []
for x in data.split('\n'):
    try:
        adapters.append(int(x))
    except ValueError:
        pass

N = len(adapters)

# Part 1: build a stack of adapters and multiply the number of 1 and 3 differences
adapters = [0] + adapters + [max(adapters) + 3]
adapters.sort()

diff_counts = {1: 0, 2: 0, 3: 0}
diffs = []
for i in range(N + 1):
    diff = adapters[i + 1] - adapters[i]
    diffs.append(diff)
    diff_counts[diff] += 1

number = diff_counts[1] * diff_counts[3]
print(f"Number: {number}")

# Part 2: determine number of possible stacks
A = [[0] * (N + 2) for _ in range(N + 2)]  # adjacency matrix

for i, a in enumerate(adapters[:-1]):
    j = 1
    while adapters[i + j] - a <= 3:
        A[i][i + j] = 1
        j += 1
        if i + j == len(adapters):
            break

def _count_paths(s, d, count=0):
    if s == d:
        count += 1
    else:
        # Count paths from adjacent nodes (those are never more than 3 away)
        for i, x in enumerate(A[s][s + 1:s + 4]):
            if x == 1:
                count = _count_paths(s + 1 + i, d, count)

    return count

combinations = 1
prev_s = 0
for i, d in enumerate(diffs):
    if d == 3:
        # Count number of paths of sub-graph
        sub_combinations = _count_paths(prev_s, i + 1)
        prev_s = i + 1
        combinations *= sub_combinations

print(f"Combinations: {combinations}")
