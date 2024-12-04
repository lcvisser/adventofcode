import re

# Read data
input_file = "2024/03/input.txt"
with open(input_file) as f:
    data = f.read()

mul = re.compile(r"mul\((\d+),(\d+)\)")
instructions = mul.findall(data)
total1 = sum(int(a) * int(b) for a, b in instructions)

# Part 1: sum of all mul() instruction results
print(f"Sum of all multiplications: {total1}")

instruction_set = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)")

total2 = 0
mul_enabled = True
for instr in instruction_set.finditer(data):
    if instr.group(0).startswith("mul") and mul_enabled:
        total2 += int(instr.group(1)) * int(instr.group(2))
    elif instr.group(0) == "do()":
        mul_enabled = True
    elif instr.group() == "don't()":
        mul_enabled = False

# Part 2: sum of all enabled mul() instruction results
print(f"Sum of all enabled multiplications: {total2}")
