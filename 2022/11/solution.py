import sys
import collections
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
        self.divisor = 0
        self.test = None
        self.target = {True: None, False: None}
        self.number_of_items_inspected = 0


def parse_input(data):
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
                    # monkey.items = collections.deque(items)
                    monkey.items = items
                elif attribute.startswith("Operation"):
                    operation = eval("lambda old: " + valuestr.split('=')[1])
                    monkey.operation = operation
                elif attribute.startswith("Test"):
                    d = int(valuestr.strip().split(' ')[2])
                    monkey.divisor = d
                    monkey.test = lambda v, divisor=d: v % divisor == 0
                elif attribute.startswith("If true"):
                    t = int(valuestr.strip().split(' ')[3])
                    monkey.target[True] = int(t)
                elif attribute.startswith("If false"):
                    t = int(valuestr.strip().split(' ')[3])
                    monkey.target[False] = int(t)

        monkeys[monkey.ident] = monkey

    return monkeys


# Play rounds for part 1
monkeys1 = parse_input(data)
for _ in range(20):
    for monkey in monkeys1.values():
        while monkey.items:
            monkey.number_of_items_inspected += 1
            value = monkey.items.pop(0)
            value = monkey.operation(value)
            value = math.floor(value / 3)
            r = monkey.test(value)
            target_monkey_id = monkey.target[r]
            monkeys1[target_monkey_id].items.append(value)

# Part 1: most monkey business
mb = sorted([m.number_of_items_inspected for m in monkeys1.values()], reverse=True)
print(f"Level of monkey business: {mb[0] * mb[1]}")

# Prepare for part 2
monkeys2 = parse_input(data)
num_items = sum(len(m.items) for m in monkeys2.values())
for monkey in monkeys2.values():
    monkey.iter = len(monkey.items)
    monkey.items.extend([0] * (num_items - len(monkey.items)))

prod_div = math.prod(m.divisor for m in monkeys2.values())

# Play rounds for part 2
for _ in range(10000):
    for monkey in monkeys2.values():
        for i in range(monkey.iter):
            monkey.number_of_items_inspected += 1
            value = monkey.items[i]
            value = int(monkey.operation(value))
            r = value % monkey.divisor
            target_monkey_id = monkey.target[r == 0]
            monkeys2[target_monkey_id].items[monkeys2[target_monkey_id].iter] = value % prod_div
            monkeys2[target_monkey_id].iter += 1

        monkey.iter = 0

# Part 2: most monkey business after a long time
mb = sorted([m.number_of_items_inspected for m in monkeys2.values()], reverse=True)
print(f"Level of monkey business: {mb[0] * mb[1]}")
