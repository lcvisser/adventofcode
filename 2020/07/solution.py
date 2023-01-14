import re
import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    rules = f.read()

# Parse the rules
rule_pattern = re.compile(r"^(.*) bags contain (no other bags|.*)\.$")
contents_pattern = re.compile(r"([0-9]+) (.*) bags?")

containers = {}
for rule in rules.split('\n'):
    rule_match = rule_pattern.match(rule)
    if rule_match:
        container_color = rule_match.group(1)
        contents = []
        if rule_match.group(2) != "no other bags":
            for c in rule_match.group(2).split(','):
                contents_match = contents_pattern.match(c.strip())
                if contents_match:
                    count = int(contents_match.group(1))
                    color = contents_match.group(2)
                    contents.append((color, count))

        containers[container_color] = contents

# Part 1: how many bags can eventually hold my bag?
my_bag = "shiny gold"
def can_hold_my_bag(_contents):
    if not _contents:
        return False
    elif my_bag in list(zip(*_contents))[0]:
        return True
    else:
        return any([can_hold_my_bag(containers[c[0]]) for c in _contents])

count = 0
for contents in containers.values():
    if can_hold_my_bag(contents):
        count += 1

print(f"Number of bags that can hold my bag: {count}")

# Part 2: how many bags do I need to bring?
def add_bags(bags):
    count = 0
    for b, n in bags:
        count += n * (1 + add_bags(containers[b]))
    return count

total_bag_count = add_bags(containers[my_bag])
print(f"Number of bags to bring: {total_bag_count}")
