import math
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

# Solve for na and nb:
#   dxa * na + dxb * nb = px
#   dya * na + dyb * nb = py
#
# These are linear Diophante equations of the form ax + by = c. They have a solution if and only if:
#   gcd(a, b) = 0 mod c
#
# If it has a solution, it can be found via the Extended Euclidean algorithm, which yields Bezout coefficients s and t
# such that:
#   as + bt = gcd(a, b)
#
# Then, there exists an integer k = c / gcd(a, b), such that
#   ask + btk = gcd(a, b) k = c
#
# The initial solution x0, y0 is thus:
#  x0 = sk, y0 = tk
#
# The family of solutions is given by, for any integer n:
#  x = x0 - n b / gcd(a, b), y = y0 + n a / gcd(a, b)
#
# (see also: https://math.stackexchange.com/a/20727)

def extended_gcd(a, b):
    """Extended Euclidean algorithm.

    See: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

    Returns: gcd(a, b), s, t, such that as + bt = gcd(a, b)
    """
    rp, rc = a, b
    sp, sc = 1, 0
    tp, tc = 0, 1
    while rc > 0:
        rp, rc, q = rc, rp % rc, rp // rc
        sp, sc = sc, sp - q * sc
        tp, tc = tc, tp - q * tc

    return rp, sp, tp


costs = 0
for m, machine in enumerate(machines):
    dxa, dya = machine["a"]
    dxb, dyb = machine["b"]
    px, py = machine["prize"]

    gcdx, ax, bx = extended_gcd(dxa, dxb)
    gcdy, ay, by = extended_gcd(dya, dyb)
    has_solution = px % gcdx == 0 and py % gcdy == 0
    if has_solution:
        # Possible solution for x coordinate:
        kx = px // gcdx
        nxa0, nxb0 = ax * kx, bx * kx

        # Possible solution for y coordinate:
        ky = py // gcdy
        nya0, nyb0 = ay * ky, by * ky

        # Solutions for the two coordinates, for free nx and ny:
        #   px = dxa * (nxa0 - nx * dxb // gcdx) + dxb * (nxb0 + nx * dxa // gcdx)
        #   py = dya * (nya0 - ny * dyb // gcdy) + dyb * (nyb0 + ny * dya // gcdy)
        #              \-- #button A presses --/         \-- #button B presses --/
        #
        # We must have (because A and B are linked):
        #   nxa0 - nx * dxb // gcdx == nya0 - ny * dyb // gcdy
        #   nxb0 + nx * dxa // gcdx == nyb0 + ny * dya // gcdy
        #
        # Finally, number of button presses should be positive

        nx_limits = [nxa0 // (dxb // gcdx), -nxb0 // (dxa // gcdx)]
        ny_limits = [nya0 // (dyb // gcdy), -nyb0 // (dya // gcdy)]
        for nx in range(min(nx_limits), max(nx_limits) + 1):
            for ny in range(min(ny_limits), max(ny_limits) + 1):
                numAx = nxa0 - nx * dxb // gcdx
                numAy = nya0 - ny * dyb // gcdy
                numBx = nxb0 + nx * dxa // gcdx
                numBy = nyb0 + ny * dya // gcdy

                if numAx == numAy and numBx == numBy:
                    costs += numAx * COST_A + numBx * COST_B
                    break  # there is only one solution!

# Part 1: total costs of tokens for winning all possible prizes
print(f"Number of tokens: {costs}")
