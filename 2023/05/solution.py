import sys
import functools

# Class to implement mapping
class Mapping:
    def __init__(self, name):
        self._name = name
        self._maps = {}

    def __repr__(self):
        r = f"Mapper({self._name}):\n"
        for s, (d, l) in self._maps.items():
            r += f"{s}:{l} -> {d}:{l}\n"
        return r

    def add_range(self, dst_range_start, src_range_start, range_length):
        self._maps[src_range_start] = (dst_range_start, range_length)

    def apply(self, n):
        for src, (dst, l) in self._maps.items():
            if n in range(src, src + l):
                d = dst + (n - src)
                break
        else:
            d = n

        return d

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
seeds = []
mappings = []
for line in data.strip().split('\n'):
    if line.strip() == "":
        continue

    if line.startswith("seeds:"):
        seeds = [int(s) for s in line[len("seeds: "):].split()]
    elif "map:" in line:
        name = line[:line.index(" map:")]
        m = Mapping(name)
        mappings.append(m)
    else:
        mappings[-1].add_range(*[int(c) for c in line.split()])

# Part 1: lowest location number
locations = []
for s in seeds:
    l = functools.reduce(lambda x, m: m.apply(x), mappings, s)
    locations.append(l)

print(f"Lowest location number: {min(locations)}")
