import sys
import itertools
import re


# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
node_matcher = re.compile(r"^([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)$")
instructions = ""
network = dict()
for i, line in enumerate(data.strip().split('\n')):
    if i == 0:
        instructions = line
    elif line == "":
        continue
    else:
        m = node_matcher.match(line)
        node = m.group(1)
        left = m.group(2)
        right = m.group(3)
        network[node] = (left, right)

# Follow instructions
n_steps = 0
curr_node = "AAA"
direction = {'L': 0, 'R': 1}
for d in itertools.cycle(instructions):
    n_steps += 1
    next_node = network[curr_node][direction[d]]
    curr_node = next_node
    if curr_node == "ZZZ":
        break

# Part 1: number of steps to go from AAA to ZZZ
print(f"Number of steps: {n_steps}")
