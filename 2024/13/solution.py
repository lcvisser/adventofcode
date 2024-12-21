import re

# Read data
input_file = "2024/13/input.txt"
with open(input_file) as f:
    data = f.read()

button = re.compile(r"[XY]\+(\d+)")
prize = re.compile(r"[XY]=(\d+)")

COST_A = 3
COST_B = 1

# Parse input
machines = []
machine = {}
for line in data.strip().split('\n'):
    if line.startswith("Button A:"):
        x_move, y_move = button.findall(line)
        machine["a"] = (int(x_move), int(y_move))
    elif line.startswith("Button B:"):
        x_move, y_move = button.findall(line)
        machine["b"] = (int(x_move), int(y_move))
    elif line.startswith("Prize:"):
        x_prize, y_prize = prize.findall(line)
        machine["prize"] = (int(x_prize), int(y_prize))
    else:
        machines.append(machine)
        machine = {}

# Add last machine in the input data
machines.append(machine)
machine = {}

# This is two equations with two unknows: solve for number of button presses na and nb:
#   dxa * na + dxb * nb = px
#   dya * na + dyb * nb = py
#
#  [ dxa  dxb]   [na]   [px]
#  [         ] x [  ] = [  ]
#  [ dya  dyb]   [nb]   [py]
#
#  det = dxa * dyb - dxb * dya
#
#  [na]    1  [ dyb -dxb]   [px]
#  [  ] = --- [         ] x [  ]
#  [nb]   det [-dya  dxa]   [py]

def compute_costs(offset=0):
    costs = 0
    for m, machine in enumerate(machines):
        dxa, dya = machine["a"]
        dxb, dyb = machine["b"]
        px, py = machine["prize"]
        px += offset
        py += offset

        det = dxa * dyb - dxb * dya
        if det != 0:
            na = 1 / det * ( dyb * px - dxb * py)
            nb = 1 / det * (-dya * px + dxa * py)

            # Check if positive number of button presses and integer number (within floating-point rounding error)
            if na > 0 and round(na) == round(na, 4) and nb > 0 and round(nb) == round(nb, 4):
                costs += na * COST_A + nb * COST_B

    return int(costs)


# Part 1: total costs of tokens for winning all possible prizes
print(f"Number of tokens: {compute_costs()}")

# Part 2: total costs of tokens for winning all possible prizes with massive offset
print(f"Number of tokens: {compute_costs(10000000000000)}")
