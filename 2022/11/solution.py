import sys
import math

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


class Monkey:
    def __init__(self):
        self.ident = None
        self.items = []
        self.operation = None
        self.test = None
        self.target = {True: None, False: None}
        self.number_of_items_inspected = 0


# Parse input data
data = data.strip().split("\n\n")
monkeys = {}
for monkey_data in data:
    monkey = Monkey()

    for descriptor in [d.strip() for d in monkey_data.split('\n')]:
        if descriptor.startswith("Monkey"):
            ident = int(descriptor[len("Monkey "):-1])
            monkey.ident = ident
        else:
            attribute, valuestr = descriptor.split(':')
            if attribute.startswith("Starting items"):
                items = [int(s) for s in valuestr.split(',')]
                monkey.items = items
            elif attribute.startswith("Operation"):
                operation = eval("lambda old: " + valuestr.split('=')[1])
                monkey.operation = operation
            elif attribute.startswith("Test"):
                d = int(valuestr.strip().split(' ')[2])
                monkey.test = lambda v, divisor=d: v % divisor == 0
            elif attribute.startswith("If true"):
                t = int(valuestr.strip().split(' ')[3])
                monkey.target[True] = int(t)
            elif attribute.startswith("If false"):
                t = int(valuestr.strip().split(' ')[3])
                monkey.target[False] = int(t)

    monkeys[monkey.ident] = monkey

# Play rounds
for _ in range(20):
    for monkey in monkeys.values():
        while monkey.items:
            item = monkey.items.pop(0)
            monkey.number_of_items_inspected += 1

            item = monkey.operation(item)
            item = math.floor(item / 3)
            r = monkey.test(item)
            target_monkey_id = monkey.target[r]
            monkeys[target_monkey_id].items.append(item)

# Part 1: most monkey business
mb = sorted([m.number_of_items_inspected for m in monkeys.values()], reverse=True)
print(f"Level of monkey business: {mb[0] * mb[1]}")
