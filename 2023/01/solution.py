import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
calibration_values1 = []
for line in data.strip().split('\n'):
    digits = [int(c) for c in line if c in "0123456789"]
    calibration_values1.append(10 * digits[0] + digits[-1])

# Part 1: sum of calibration values
print(f"Sum of calibration values: {sum(calibration_values1)}")


text_to_numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

calibration_values2 = []
for line in data.strip().split('\n'):
    digits = []
    token = ""
    for c in line:
        if c in "0123456789":
            digits.append(int(c))
            token = ""
        else:
            token += c
            found = [token.find(k) >= 0 for k in text_to_numbers.keys()]
            if any(found):
                key_index = found.index(True)
                number = list(text_to_numbers.values())[key_index]

                digits.append(number)
                token = c  # numbers are allowed to overlap (!)

    calibration_values2.append(10 * digits[0] + digits[-1])

# Part 2: sum of calibration values
print(f"Sum of calibration values: {sum(calibration_values2)}")
