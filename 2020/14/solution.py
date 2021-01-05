import sys
from itertools import product

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse instructions
instructions = []
for line in data.split('\n'):
    if len(line) == 0:
        pass
    else:
        instr, arg = line.split(" = ")
        if instr.startswith("mask"):
            instructions.append(("mask", arg))
        elif instr.startswith("mem"):
            address = int(instr[len("mem["):-1])
            value = int(arg)
            instructions.append(("mem", (address, value)))
        else:
            raise ValueError("Invalid instruction: {}".format(instr))

# Part 1: apply bit masks to the values written to memory
mask_dontcares = 0
mask_set = 0
mem = {}
for instr, arg in instructions:
    if instr == "mask":
        mask_dontcares = 0
        mask_set = 0
        for i, c in enumerate(arg[::-1]):
            if c == 'X':
                mask_dontcares |= 1 << i
            else:
                mask_set |= int(c) << i
    elif instr == "mem":
        address, value = arg
        value &= mask_dontcares
        value |= mask_set
        mem[address] = value
    else:
        pass

sum_of_data = sum(mem.values())
print(f"Sum: {sum_of_data}")

# Part 2: apply the bit masks to the memory address
mask_dontcares = [(0, 0)]
mask_set = 0
mem = {}
for instr, arg in instructions:
    if instr == "mask":
        masked_idx = []
        mask_set = 0
        for i, c in enumerate(arg[::-1]):
            if c == 'X':
                masked_idx.append(i)
            else:
                mask_set |= int(c) << i

        mask_dontcares = []
        for mask in product([0, 1], repeat=len(masked_idx)):
            m_reset = 0
            m_permute = 0
            for j, k in zip(masked_idx, mask):
                m_reset |= 1 << j
                m_permute |= k << j
            mask_dontcares.append((m_reset, m_permute))
    elif instr == "mem":
        address, value = arg
        address |= mask_set
        for m_reset, m_permute in mask_dontcares:
            address &= ~m_reset
            address |= m_permute
            mem[address] = value
    else:
        pass

sum_of_data = sum(mem.values())
print(f"Sum: {sum_of_data}")
