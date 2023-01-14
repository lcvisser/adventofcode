import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

cals_per_elf = [0]
elf_number = 0
for line in lines:
    if line.strip() == "":
        cals_per_elf.append(0)
        elf_number += 1
    else:
        cals = int(line)
        cals_per_elf[elf_number] += cals

# Part 1: maximum number of calories carried
max_cals = sorted(cals_per_elf)[-1]
print(f"Max. number of calories carried: {max_cals}")

# Part 2: sum of maximum number of calories carried of top three
max_cals3 = sorted(cals_per_elf)[-3:]
print(f"Max. number of calories carried by top 3: {sum(max_cals3)}")
