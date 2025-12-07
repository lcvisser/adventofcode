from functools import reduce
from operator import add, mul

with open("2025/06/input.txt") as f:
    data = f.read()

homework = data.strip().split("\n")
inputs = [r.split() for r in homework]
problems = zip(*inputs)

# Part 1
grand_total = 0
for p in problems:
    operands = [int(v) for v in p[:-1]]
    operator = {"+": add, "*": mul}[p[-1]]
    result = reduce(operator, operands)
    grand_total += result

print(f"Grand total: {grand_total}")
