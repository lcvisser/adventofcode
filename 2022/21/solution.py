import sys
import operator
import re

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()



data_ex = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

# Parse data
yell_number = re.compile(r"^([0-9]+)$")
do_operation = re.compile(r"^([a-z]{4}) ([\+\-\*\/]{1}) ([a-z]{4})$")

monkeys = {}
dependencies = []
for line in data.strip().split('\n'):
    monkey, job = line.split(": ")
    number = yell_number.match(job)
    if number is not None:
        monkeys[monkey] = int(number[0])
    else:
        operation = do_operation.match(job)
        operand1, op, operand2 = operation.groups()
        match op:
            case '+':
                f = operator.add
            case '-':
                f = operator.sub
            case '*':
                f = operator.mul
            case '/':
                f = operator.truediv
            case _:
                raise ValueError(op)

        dependencies.append((monkey, operand1, operand2, f))

# Resolve dependecies
while dependencies:
    target, op1, op2, f = dependencies.pop(0)
    if op1 in monkeys.keys() and op2 in monkeys.keys():
        ans = f(monkeys[op1], monkeys[op2])
        monkeys[target] = ans
    else:
        dependencies.append((target, op1, op2, f))

# Part 1: what will root yell?
answer = int(monkeys["root"])
print(f"root yells: {answer}")
