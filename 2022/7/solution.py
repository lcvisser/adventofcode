import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

dirsizes = {}
pwd = []
for line in lines:
    if line.startswith("$ cd"):
        _, cmd, arg = line.split(' ')
        if arg == "..":
            pwd.pop()
        else:
            pwd.append(arg)
            key = ':'.join(pwd)
            if key not in dirsizes:
                dirsizes[key] = 0
    elif line.startswith("$ ls"):
        pass  # nothing to do
    else:
        ls = line.split(' ')
        if ls[0] != "dir":
            size = int(ls[0])
            for i in range(1, len(pwd) + 1):
                key = ':'.join(pwd[:i])
                dirsizes[key] += size
        else:
            pass  # directory has no size

# Part 1: total size of directories not exceeding 100000
max_size = 100000
total_size = sum(filter(lambda x: x <= max_size, dirsizes.values()))
print(f"Sum of directory sizes: {total_size}")
