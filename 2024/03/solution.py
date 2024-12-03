import re

# Read data
input_file = "2024/03/input.txt"
with open(input_file) as f:
    data = f.read()

mul = re.compile(r"mul\((\d+),(\d+)\)")
instructions = mul.findall(data)
total = sum(int(a) * int(b) for a, b in instructions)

# Part 1: sum of all mul() instruction results
print(f"Sum of all multiplications: {total}")
