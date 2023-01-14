import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Part 1: how many are valid if the policy indicates the occurence of the required character?
valid_count = 0
for entry in data.split('\n'):
    try:
        policy, password = entry.split(':')
    except ValueError:
        continue
    password = password.strip()
    req_count, req_char = policy.split()
    req_count_min, req_count_max = [int(x) for x in req_count.split('-')]
    char_count = password.count(req_char)
    if req_count_min <= char_count <= req_count_max:
        valid_count += 1

print(f"Number of valid passwords: {valid_count}")

# Part 2: how many are valid if the policy indicates the position of the required character?
valid_count = 0
for entry in data.split('\n'):
    try:
        policy, password = entry.split(':')
    except ValueError:
        continue
    password = password.strip()
    req_loc, req_char = policy.split()
    req_locs = [int(x) - 1 for x in req_loc.split('-')]  # 1-indexed

    try:
        loc1_ok = password[req_locs[0]] == req_char
    except IndexError:
        loc1_ok = False

    try:
        loc2_ok = password[req_locs[1]] == req_char
    except IndexError:
        loc2_ok = False

    if (loc1_ok or loc2_ok) and not (loc1_ok and loc2_ok):
        valid_count += 1

print(f"Number of valid passwords: {valid_count}")
