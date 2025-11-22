import re

INVALID_LETTERS = "iol"
PAIR = re.compile(r"([a-z])\1")

def increment_letter(c):
    n = ord(c) - ord("a")  # a = 0, b = 1, ...
    d, r = divmod(n + 1, 26)
    return d > 0, chr(r + ord("a"))


def increment_letter_to_valid(c):
    carry, new_c = increment_letter(c)
    while new_c in INVALID_LETTERS:
        carry, new_c = increment_letter(new_c)

    return carry, new_c


def increment_string(s):
    c = s[-1]
    carry, new_c = increment_letter_to_valid(c)
    new_s = new_c
    for c in reversed(s[:-1]):
        if carry:
            carry, new_c = increment_letter_to_valid(c)
        else:
            new_c = c

        new_s = new_c + new_s

    if carry:
        new_s = "a" + new_s

    return new_s


def has_straight_sequence(password):
    for i in range(len(password) - 3):
        subset = password[i:i + 3]
        subset_numbers = [ord(c) for c in subset]
        is_sequential = [subset_numbers[i + 1] - subset_numbers[i] == 1 for i in range(len(subset_numbers) - 1)]
        has_sequence = all(is_sequential)
        if has_sequence:
            break
    else:
        has_sequence = False

    return has_sequence


def has_no_invalid_chars(password):
    return all(c not in INVALID_LETTERS for c in password)


def has_two_pairs(password):
    return len(PAIR.findall(password)) >= 2


def is_valid_password(password):
    return has_straight_sequence(password) and has_no_invalid_chars(password) and has_two_pairs(password)


def find_next_password(password):
    new_password = increment_string(password)
    while not is_valid_password(new_password):
        new_password = increment_string(new_password)

    return new_password

# Part 1
print(f"New password: {find_next_password("vzbxkghb")}")
