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

def _process(_i, _accumulator, _instr, _arg):
    if _instr == "acc":
        _accumulator += _arg
        _i += 1
    elif _instr == "jmp":
        _i += _arg
    elif _instr == "nop":
        _i += 1

    return _i, _accumulator

# Part 1: accumulator value just before second instruction execution
accumulator = 0
lines_visited = []
i = 0
while i not in lines_visited:
    instr, arg = program[i]
    lines_visited.append(i)
    i, accumulator = _process(i, accumulator, instr, arg)

print(f"Accumulator: {accumulator}")

# Part 2: change one nop into an acc or vice versa to make the program terminate
def run_to_end(_i, _program, _history):
    lines_visited = _history.copy()
    accumulator = 0
    while True:
        if _i in lines_visited:
            # Stuck in loop
            return None, lines_visited

        if _i > len(program):
            # Too far
            return None, lines_visited

        if _i == len(_program):
            # Terminated
            return accumulator, lines_visited

        instr, arg = _program[_i]
        lines_visited.append(_i)
        _i, accumulator = _process(_i, accumulator, instr, arg)

accumulator = 0
lines_visited = []
i = 0
while True:
    instr, arg = program[i]
    lines_visited.append(i)

    if instr == "acc":
        accumulator += arg
        i += 1
    elif instr == "jmp":
        # Change into NOP and see if the program terminates
        i += 1
        new_accumulator, new_lines_visited = run_to_end(i, program, lines_visited)
        if new_accumulator is None:
            # Failure; undo and resume as if we did a jump instruction
            i -= 1
            i += arg
        else:
            # Success
            accumulator += new_accumulator
            break
    elif instr == "nop":
        # Change into a JMP and see if the program terminates
        i += arg
        new_accumulator, new_lines_visited = run_to_end(i, program, lines_visited)
        if new_accumulator is None:
            # Failure; undo and resume as if we did a nop instruction
            i -= arg
            i += 1
        else:
            # Succsess
            accumulator += new_accumulator
            break

print(f"Accumulator: {accumulator}")
