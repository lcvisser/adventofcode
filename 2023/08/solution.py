import sys
import itertools
import math
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

direction = {'L': 0, 'R': 1}

# Follow instructions
n_steps1 = 0
curr_node = "AAA"
for d in itertools.cycle(instructions):
    n_steps1 += 1
    curr_node = network[curr_node][direction[d]]
    if curr_node == "ZZZ":
        break

# Part 1: number of steps to go from AAA to ZZZ
print(f"Number of steps: {n_steps1}")

# Follow ghost instructions
n_steps2 = []
start_nodes = [n for n in network.keys() if n.endswith('A')]
end_nodes = [n for n in network.keys() if n.endswith('Z')]
for c in start_nodes:
    n_steps2.append(0)
    curr_node = c
    for d in itertools.cycle(instructions):
        n_steps2[-1] += 1
        curr_node = network[curr_node][direction[d]]
        # Find a path that ends on a Z node after one or more cycles of the instructions; when found, the least common
        # multiple of all such cycles is the answer
        if curr_node in end_nodes and n_steps2[-1] % len(instructions) == 0:
            break

# Part 2: number of ghost steps from A to Z
print(f"Number of ghost steps: {math.lcm(*n_steps2)}")
