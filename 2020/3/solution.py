import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

input_map = data

# Part 1: count number of trees for slope down 1, right 3
c = 0
n_trees = 0
for row in input_map.split():
    if row[c] == '#':
        n_trees += 1
    c = (c + 3) % len(row)

print(f"Number of trees: {n_trees}")

# Part 2: count number of trees for varying slopes and compute product of counts
def count_trees(_map, _slope):
    right, down = _slope
    c = 0
    n_trees = 0
    for row in _map[::down]:
        if row[c] == '#':
            n_trees += 1
        c = (c + right) % len(row)
    return n_trees

solution = 1
for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    n_trees = count_trees(input_map.split(), slope)
    print("Number of trees for slope right {}, down {}: {}".format(*slope, n_trees))
    solution *= n_trees

print(f"Solution: {solution}")
