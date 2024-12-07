import operator

# Read data
input_file = "2024/07/input.txt"
with open(input_file) as f:
    data = f.read()


OPERATORS = {
    "+": operator.add,
    "*": operator.mul
}


# Helper function to search for a possible combination of operands that yields the right result
def can_be_true(target, operands):
    to_try = [(0, operands.copy(), "+"), (0, operands.copy(), "*")]
    while to_try:
        current_value, numbers, op = to_try.pop(0)
        next_number = numbers.pop(0)
        new_value = OPERATORS[op](current_value, next_number)
        if numbers:
            to_try.append((new_value, numbers.copy(), "+"))
            to_try.append((new_value, numbers.copy(), "*"))
        else:
            if new_value == target:
                return True

    return False


# Parse and process
total = 0
for line in data.strip().split('\n'):
    target_str, operands_str = line.split(':')
    target = int(target_str)
    operands = [int(x) for x in operands_str.split()]
    if can_be_true(target, operands):
        total += target

# Part 1: sum of calibration values that can be achieved
print(f"Total calibration result: {total}")
