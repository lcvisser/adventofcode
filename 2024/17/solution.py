# Read data
input_file = "2024/17/input.txt"
with open(input_file) as f:
    data = f.read()

registers = {}
output = []
program = []

for line in data.strip().split('\n'):
    if line.startswith("Register A:"):
        _, v = line.split(':')
        registers['A'] = int(v)
    elif line.startswith("Register B:"):
        _, v = line.split(':')
        registers['B'] = int(v)
    elif line.startswith("Register C:"):
        _, v = line.split(':')
        registers['C'] = int(v)
    elif line.startswith("Program:"):
        _, p = line.split(':')
        program = [int(x) for x in p.split(',')]


def get_combo_value(combo):
    match combo:
        case 0 | 1 | 2 | 3:
            value = combo
        case 4:
            value = registers['A']
        case 5:
            value = registers['B']
        case 6:
            value = registers['C']
        case 7:
            raise ValueError

    return value

pointer = 0
try:
    while pointer < len(program):
        opcode = program[pointer]
        match opcode:
            case 0:
                # adv
                num = registers['A']
                combo = program[pointer + 1]
                den = get_combo_value(combo)
                registers['A'] = num >> den
                pointer += 2
            case 1:
                # bxl
                lit = program[pointer + 1]
                registers['B'] ^= lit
                pointer += 2
            case 2:
                # bst
                combo = program[pointer + 1]
                value = get_combo_value(combo)
                registers['B'] = value & 0x7
                pointer += 2
            case 3:
                # jnz
                if registers['A'] == 0:
                    # do nothing
                    pointer += 1
                else:
                    jump_to = program[pointer + 1]
                    pointer = jump_to
            case 4:
                # bxc
                registers['B'] ^= registers['C']
                pointer += 2
            case 5:
                # out
                combo = program[pointer + 1]
                value = get_combo_value(combo)
                output.append(value & 0x7)
                pointer += 2
            case 6:
                # bdv
                num = registers['A']
                combo = program[pointer + 1]
                den = get_combo_value(combo)
                registers['B'] = num >> den
                pointer += 2
            case 7:
                # cdv
                num = registers['A']
                combo = program[pointer + 1]
                den = get_combo_value(combo)
                registers['C'] = num >> den
                pointer += 2
except IndexError:
    pass

# Part 1: program output
print(f"Program output: {','.join(str(x) for x in output)}")
