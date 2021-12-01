import sys
from math import prod

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# data = """class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19

# your ticket:
# 11,12,13

# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9"""

sections = data.split("\n\n")

# Parse fields and values
valid_ranges = {}
for line in sections[0].split('\n'):
    field, values = line.split(':')
    valid_ranges[field] = []
    for range_str in values.split(" or "):
        lower, upper = [int(v) for v in range_str.strip().split('-')]
        valid_ranges[field].append((lower, upper))

# Part 1: scan for invalid tickets
rate = 0
invalid_tickets = []
for t, line in enumerate(sections[2].split('\n')[1:]):
    if len(line) == 0:
        continue

    values = [int(v) for v in line.split(',')]
    for v in values:
        validated = False
        for field, ranges in valid_ranges.items():
            if validated:
                break

            for lower, upper in ranges:
                if lower <= v <= upper:
                    validated = True
                    break

        if not validated:
            rate += v
            invalid_tickets.append(t)

print(f"Rate: {rate}")

# Part 2: determine ticket fields
ticket_fields = {}
for t, line in enumerate(sections[2].split('\n')[1:]):
    if len(line) == 0:
        continue

    if t in invalid_tickets:
        continue

    values = [int(v) for v in line.split(',')]
    for i, v in enumerate(values):
        if i not in ticket_fields.keys():
            ticket_fields[i] = {"valid": [], "invalid": []}

        for field, ranges in valid_ranges.items():
            for lower, upper in ranges:
                if lower <= v <= upper:
                    if field not in ticket_fields[i]["valid"] and field not in ticket_fields[i]["invalid"]:
                        ticket_fields[i]["valid"].append(field)
                    break
            else:
                if field in ticket_fields[i]["valid"]:
                    ticket_fields[i]["valid"].remove(field)
                if field not in ticket_fields[i]["invalid"]:
                    ticket_fields[i]["invalid"].append(field)


field_ids = []
valid_fields = []
invalid_fields = []
for i in ticket_fields:
    field_ids.append(i)
    valid_fields.append(ticket_fields[i]["valid"])
    invalid_fields.append(ticket_fields[i]["invalid"])

ticket = list(zip(field_ids, valid_fields, invalid_fields))
n = 0
while not all(len(x[1]) == 1 for x in ticket):
    ticket.sort(key=lambda x: len(x[1]))
    assert len(ticket[n][1]) == 1
    field_to_pop = ticket[n][1][0]
    for t in ticket[n + 1:]:
        assert len(t[1]) > 1
        if field_to_pop in t[1]:
            t[1].remove(field_to_pop)
    n += 1

ticket_field_names = [x[1][0] for x in ticket]
my_ticket_values = [int(v) for v in sections[1].split('\n')[1].split(',')]
assert len(ticket_field_names) == len(my_ticket_values)

my_ticket = {f: v for f, v in zip(ticket_field_names, my_ticket_values)}
print(my_ticket)

number = prod([v for f, v in my_ticket.items() if f.startswith("departure")])
print(f"Number: {number}")
