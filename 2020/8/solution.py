import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    code = f.read()


# Parse program source code
program = []
for line in code.split('\n'):
    try:
        instr, arg = line.split(' ')
        arg = int(arg)
        program.append((instr, arg))
    except ValueError:
        pass

# Part 1: accumulator value just before second instruction execution
accumulator = 0
lines_visited = []
i = 0
while i not in lines_visited:
    instr, arg = program[i]
    lines_visited.append(i)
    if instr == "acc":
        accumulator += arg
        i += 1
    elif instr == "jmp":
        i += arg
    elif instr == "nop":
        i += 1

print(f"Accumulator: {accumulator}")
