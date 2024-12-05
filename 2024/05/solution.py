# Read data
input_file = "2024/05/input.txt"
with open(input_file) as f:
    data = f.read()


rules_str, updates = data.strip().split("\n\n")

rules = []
for rule in rules_str.split('\n'):
    p, q = rule.split('|')
    rules.append((int(p), int(q)))

sum__of_middle_pages = 0
for line in updates.split('\n'):
    update = [int(x) for x in line.split(',')]
    applicable_rules = filter(lambda t: t[0] in update and t[1] in update, rules)
    correct = [update.index(p) < update.index(q) for p, q in applicable_rules]
    if all(correct):
        middle_page = update[len(update) // 2]
        sum__of_middle_pages += middle_page

# Part 1: sum of middle page numbers for correct updates
print(f"Sum of middle page numbers for correct updates: {sum__of_middle_pages}")
