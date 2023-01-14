import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
initial_positions = [int(x) for x in data.strip().split(',')]
max_position = max(initial_positions)

# Determine linear fuel costs per position
costs = [[0] * max_position for _ in range(len(initial_positions))]
for i, p in enumerate(initial_positions):
    for x in range(max_position):
        costs[i][x] = abs(p - x)

# Part 1: find minimum total cost
total_costs_per_position = [sum(c) for c in zip(*costs)]
print("Optimal cost={}".format(min(total_costs_per_position)))

# Determine nonlinear fuel costs per position
costs = [[0] * max_position for _ in range(len(initial_positions))]
for i, p in enumerate(initial_positions):
    for x in range(max_position):
        costs[i][x] = sum(range(1, abs(p - x) + 1))

# Part 2: find minimum total cost
total_costs_per_position = [sum(c) for c in zip(*costs)]
print("Optimal cost={}".format(min(total_costs_per_position)))
