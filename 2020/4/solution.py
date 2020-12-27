import re
import sys

from functools import partial

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

passports = data.split('\n\n')

# Validation functions
def year_is_valid(range_lower, range_upper, x):
    return range_lower <= int(x) <= range_upper

def height_is_valid(x):
    try:
        hgt = int(x[:-2])
        unit = x[-2:]
    except ValueError:
        return False

    if unit == 'cm':
        return 150 <= hgt <= 193
    elif unit == 'in':
        return 59 <= hgt <= 76
    else:
        return False

valid_color = re.compile('^#[0-9a-f]{6}$')
valid_pid = re.compile('^[0-9]{9}$')

# Required fields with validator mapping
req_fields = {
    "byr": partial(year_is_valid, 1920, 2002),
    "iyr": partial(year_is_valid, 2010, 2020),
    "eyr": partial(year_is_valid, 2020, 2030),
    "hgt": height_is_valid,
    "hcl": lambda x: valid_color.match(x),
    "ecl": lambda x: x in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
    "pid": lambda x: valid_pid.match(x),
}

# Part 1: count number of passports with all required fields
valid_passport_count = 0
for passport in passports:
    pp = [key for key, _ in map(lambda x: x.split(':'), passport.split())]
    if all(f in pp for f in req_fields.keys()):
        valid_passport_count += 1

print(f"Number of complete passports: {valid_passport_count}")

# Part 2: count number of valid passports
valid_passport_count = 0
for passport in passports:
    pp = {key: req_fields.get(key, lambda x: True)(value) for key, value in map(lambda x: x.split(':'), passport.split())}
    if all(f in pp.keys() for f in req_fields.keys()) and all(pp.values()):
        valid_passport_count += 1

print(f"Number of valid passports: {valid_passport_count}")
