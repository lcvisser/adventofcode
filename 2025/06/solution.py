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

# Part 2
homework = data.strip("\n").split("\n")
problems = zip(*homework)

grand_total = 0
operands = []
operator = None
for p in reversed(list(problems)):
    if all(v == " " for  v in p):
        continue

    n = len(p)
    digits = []
    for i, v in enumerate(p):
        if i < n - 1 and v != " ":
            digits = [10 * d for d in digits]
            digits.append(int(v))

        if i == n - 2:
            operands.append(sum(digits))
            digits = []

        if i == n - 1 and v in "+*":
            operator = {"+": add, "*": mul}[v]
            result = reduce(operator, operands)
            grand_total += result
            operands = []
            operator = None

print(f"Grand total: {grand_total}")
