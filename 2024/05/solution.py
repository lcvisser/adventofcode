import functools

# Read data
input_file = "2024/05/input.txt"
with open(input_file) as f:
    data = f.read()


rules_str, updates = data.strip().split("\n\n")

rules = []
for rule in rules_str.split('\n'):
    p, q = rule.split('|')
    rules.append((int(p), int(q)))

correct_updates = []
incorrect_updates = []
for line in updates.split('\n'):
    update = [int(x) for x in line.split(',')]
    applicable_rules = filter(lambda t: t[0] in update and t[1] in update, rules)
    correct = [update.index(p) < update.index(q) for p, q in applicable_rules]

    if all(correct):
        correct_updates.append(update)
    else:
        incorrect_updates.append(update)

sum_of_middle_pages1 = 0
for update in correct_updates:
    middle_page = update[len(update) // 2]
    sum_of_middle_pages1 += middle_page

# Part 1: sum of middle page numbers for correct updates
print(f"Sum of middle page numbers for correct updates: {sum_of_middle_pages1}")

def compare(p, q, rules):
    if q in [qq for pp, qq in rules if pp == p]:
        return -1
    else:
        return 1


sum_of_middle_pages2 = 0
for update in incorrect_updates:
    applicable_rules = list(filter(lambda t: t[0] in update and t[1] in update, rules))
    update.sort(key=functools.cmp_to_key(lambda p, q, rules=applicable_rules: compare(p, q, rules)))

    middle_page = update[len(update) // 2]
    sum_of_middle_pages2 += middle_page

# Part 2: sum of middle page numbers for corrected updates
print(f"Sum of middle page numbers for corrected updates: {sum_of_middle_pages2}")
