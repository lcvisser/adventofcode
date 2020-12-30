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

diffs = {1: 0, 2: 0, 3: 0}
for i in range(N + 1):
    diff = adapters[i + 1] - adapters[i]
    diffs[diff] += 1

number = diffs[1] * diffs[3]
print(f"Number: {number}")
