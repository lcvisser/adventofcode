import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


# Convert from SNAFU to decimal
def from_snafu(s):
    n = 0
    for x, d in enumerate(reversed(s)):
        match d:
            case '=':
                n += -2 * 5 ** x
            case '-':
                n += -1 * 5 ** x
            case _:
                n += int(d) * 5 ** x

    return n


# Convert decimal to SNAFU
def to_snafu(n):
    # Convert to base 5; first find the highest power of 5 that fits n to determine how many digits are needed
    x = 0
    while 5 ** x - 1 < n:
        x += 1

    # Determine the digits in base 5; start with the highest power and increase until allowed maximum and then move on
    # to a lower power
    digits = [0]  # at least one digit
    for p in reversed(range(x)):
        d = 0
        while (d + 1) * 5 ** p - 1 < n:
            d += 1
        n -= d * 5 ** p
        digits.append(d)

    # If any digit is > 2, borrow from the next highest power
    s = ''
    i = len(digits) - 1
    while i >= 0:
        d = digits[i]
        match d:
            case 0 | 1 | 2:
                s += str(d)
                i -= 1
            case 3 | 4:
                s += "-="[4 - d]
                digits[i - 1] += 1
                i -= 1
            case _:
                # We have already been borrowed, propagate until we are in range 0..4 again
                digits[i] -= 5
                digits[i - 1] += 1

    # The string is in the wrong order, since we built it strarting from the highest power of 5; reverse it
    number = s[::-1]
    if len(number) > 1 and number.startswith('0'):
        number = number[1:]

    return number


# Parse input: convert SNAFU to digital
numbers = []
for line in data.strip().split('\n'):
    numbers.append(from_snafu(line))

# Part 1: compute sum and convert to SNAFU
total = sum(numbers)
total_snafu = to_snafu(total)
print(f"Total: {total_snafu}")

# Part 2: no part 2, finished :-)
