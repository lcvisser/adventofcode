import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

def assignment_to_sectors(assignment):
    first, last = [int(a) for a in assignment.split('-')]
    sectors = set(range(first, last + 1))
    return sectors


# Part 1: find overlapping pair assignments
double_assigned_count = 0
for line in lines:
    assignment1, assignment2 = line.split(',')
    sectors1 = assignment_to_sectors(assignment1)
    sectors2 = assignment_to_sectors(assignment2)
    if sectors1.issubset(sectors2) or sectors2.issubset(sectors1):
        double_assigned_count += 1

print(f"Number of double assignments: {double_assigned_count}")

# Part 2: find partly overlapping pair assignments
double_assigned_count = 0
for line in lines:
    assignment1, assignment2 = line.split(',')
    sectors1 = assignment_to_sectors(assignment1)
    sectors2 = assignment_to_sectors(assignment2)
    if sectors1 & sectors2:
        double_assigned_count += 1

print(f"Number of partly double assignments: {double_assigned_count}")
