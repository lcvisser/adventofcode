import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
program = data.strip().split('\n')

# Prepare
reg = 1
cycle = 1
reg_values_at_cycle = {s: 0 for s in (20, 60, 100, 140, 180, 220)}
stack = []

# Run program
while program:
    # Start of cycle: get next instruction if not busy
    if not stack:
        cmd = program.pop(0)
        if cmd.startswith("addx"):
            value = int(cmd.split(' ')[1])
            stack = [0, value]
        else:
            stack = [0]

    # During cycle: check registry value
    if cycle in reg_values_at_cycle.keys():
        reg_values_at_cycle[cycle] = reg

    # End of cycle: process work on stack
    if stack:
        v = stack.pop(0)
        reg += v

    cycle += 1

# Part 1: sum of signal strengths
signal_strengths = [s * v for s, v in reg_values_at_cycle.items()]
sum_of_signal_strengths = sum(signal_strengths)
print(f"Sum of signal strengths: {sum_of_signal_strengths}")
