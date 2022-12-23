import sys
import math
import operator
import re

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

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

# Part 2: figure out what to yell
class Monkey:
    def __init__(self, name):
        self.name = name
        self.oper = None
        self.oper_sym = ''
        self.value = None
        self.op1 = None
        self.op2 = None

# Parse again all the data
monkeys = {}
for line in data.strip().split('\n'):
    monkey, job = line.split(": ")
    number = yell_number.match(job)
    if number is not None:
        monkeys[monkey] = (int(number[0]), None, None, op)
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

        monkeys[monkey] = (operand1, operand2, f, op)

# Build a tree starting from root
op1, op2, *_ = monkeys["root"]
root = Monkey("root")

def build_tree(root, op, monkeys, side):
    human_found = False
    to_add = [(op, root, side)]
    while to_add:
        v, parent, parent_op = to_add.pop(0)
        m = Monkey(v)
        setattr(parent, parent_op, m)

        if v == "humn":
            human_found = True

        op1, op2, f, sym = monkeys[v]
        m.oper_sym = sym
        if op2 is None:
            m.value = op1
        else:
            m.oper = f
            to_add.append((op1, m, "op1"))
            to_add.append((op2, m, "op2"))

    return human_found

human_found1 = build_tree(root, monkeys["root"][0], monkeys, "op1")
human_found2 = build_tree(root, monkeys["root"][1], monkeys, "op2")

match (human_found1, human_found2):
    case (True, False):
        human_side = "op1"
        monkey_side = "op2"
    case (False, True):
        monkey_side = "op1"
        human_side = "op2"
    case _:
        raise ValueError(human_found1, human_found2)

# Traverse the monkey side to figure out what we need to yell
def compute(node):
    if node.name == "humn":
        node.value = float("nan")

    if node.value is None:
        # Recursively compute the node values for each operand
        op1 = compute(node.op1)
        op2 = compute(node.op2)
        node.value = node.oper(op1, op2)

    return node.value

req = int(compute(getattr(root, monkey_side)))

# Try to compute the human side - this will mark all nodes that depend on the human with NaN
have = compute(getattr(root, human_side))

# Traverse the human side to decide what we need to yell
def inv_compute(node, req):
    if math.isnan(node.value):
        node.value = req

    if node.name == "humn":
        print(f"Human needs to yell: {int(req)}")
        return

    if math.isnan(node.op1.value):
        assert not math.isnan(node.op2.value)
        match node.oper_sym:
            case '+':
                req_op1 = node.value - node.op2.value
            case '-':
                req_op1 = node.value + node.op2.value
            case '*':
                req_op1 = node.value / node.op2.value
            case '/':
                req_op1 = node.value * node.op2.value
            case _:
                raise ValueError(node.oper_sym)

        inv_compute(node.op1, req_op1)
    elif math.isnan(node.op2.value):
        assert not math.isnan(node.op1.value)
        match node.oper_sym:
            case '+':
                req_op2 = node.value - node.op1.value
            case '-':
                req_op2 = node.op1.value - node.value
            case '*':
                req_op2 = node.value / node.op1.value
            case '/':
                req_op2 = node.op1.value / node.value
            case _:
                raise ValueError(node.oper_sym)

        inv_compute(node.op2, req_op2)
    else:
        raise RuntimeError("both op1 and op2 are unknown")

inv_compute(getattr(root, human_side), req)
