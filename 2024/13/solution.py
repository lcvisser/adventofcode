import math
import re

# Read data
input_file = "2024/13/input.txt"
with open(input_file) as f:
    data = f.read()

data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

OFFSET = 10000000000000
OFFSET = 0



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
        machine["prize"] = (int(x_prize) + OFFSET, int(y_prize) + OFFSET)
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
# These are linear Diophantine equations of the form ax + by = c. They have a solution if and only if:
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

    # Prepare to solve dxa * ax + dxb * bx = px
    gcdx, ax, bx = extended_gcd(dxa, dxb)
    dx, rx = divmod(px, gcdx)

    # Prepare to solve dya * ay + dyb * by = py
    gcdy, ay, by = extended_gcd(dya, dyb)
    dy, ry = divmod(py, gcdy)

    has_solution = rx % gcdx == 0 and ry % gcdy == 0
    if has_solution:
        # Possible solution for x coordinate:
        kx = rx // gcdx + dx
        nxa0, nxb0 = ax * kx, bx * kx

        # Possible solution for y coordinate:
        ky = ry // gcdy + dy
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
