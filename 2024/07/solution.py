import operator

# Read data
input_file = "2024/07/input.txt"
with open(input_file) as f:
    data = f.read()


OPERATORS = {
    "+": operator.add,
    "*": operator.mul,
    "||": lambda a, b: int(str(a) + str(b))
}


# Helper function to search for a possible combination of operands that yields the right result
def can_be_true(target, operands, operators):
    to_try = [(0, operands.copy(), op) for op in operators]
    while to_try:
        current_value, numbers, op = to_try.pop(0)
        next_number = numbers.pop(0)
        new_value = OPERATORS[op](current_value, next_number)
        if numbers:
            for op in operators:
                to_try.insert(0, (new_value, numbers.copy(), op))
        else:
            if new_value == target:
                return True

    return False


# Parse and process
total1 = 0
total2 = 0
for line in data.strip().split('\n'):
    target_str, operands_str = line.split(':')
    target = int(target_str)
    operands = [int(x) for x in operands_str.split()]

    # Part 1: use only + and *
    if can_be_true(target, operands, ["+", "*"]):
        total1 += target

    # Part 2: use +, * and ||
    if can_be_true(target, operands, ["+", "*", "||"]):
        total2 += target

# Part 1: sum of calibration values that can be achieved with + and *
print(f"Total calibration result using + and *: {total1}")

# Part 2: sum of calibration values that can be achieved with +, * and ||
print(f"Total calibration result using +, * and ||: {total2}")
