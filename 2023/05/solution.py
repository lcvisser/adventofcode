import sys
import functools


class Mapping:
    def __init__(self, name):
        self._name = name
        self._maps = {}
        self._map_src = []

    def add_range(self, dst_range_start, src_range_start, range_length):
        # Add a mapping range, keeping it sorted by start of range
        self._maps[src_range_start] = (dst_range_start, range_length)
        self._map_src = sorted(self._maps.keys())

    def apply(self, n):
        for src, (dst, l) in self._maps.items():
            if n in range(src, src + l):
                d = dst + (n - src)
                break
        else:
            d = n

        return d

    def apply_range(self, start, length, mapped=None, map_index=0):
        if mapped is None:
            mapped = []

        if map_index >= len(self._map_src):
            # No more mappings, so leave range unchanged
            r = (start, length)
            mapped.append(r)
            return mapped

        # Apply the mapping of the given index
        map_src = self._map_src[map_index]
        map_dst, map_len = self._maps[map_src]
        if start + length - 1 < map_src:
            # Entire range is before the start of the mapping range; go to next mapping
            return self.apply_range(start, length, mapped, map_index + 1)
        elif start > map_src + map_len - 1:
            # The range is outside the current mapping range; go to next mapping
            return self.apply_range(start, length, mapped, map_index + 1)
        else:
            # The range is (partly) overlapping with the current mapping range
            if start < map_src:
                # Outside part; go to next mapping
                outside_len = map_src - start
                r_before = self.apply_range(start, outside_len, mapped, map_index + 1)
                mapped.extend(r_before)

                # Overlapping part starts at start of the mapping range
                start = map_src
                length = length - outside_len

            # Apply mapping for overlapping part
            offset = start - map_src
            if start + length <= map_src + map_len:
                # Entire range fits inside the mapping range
                r = (map_dst + offset, length)
                mapped.append(r)
                return mapped
            else:
                # Partly inside
                r = (map_dst + offset, map_len - offset)
                mapped.append(r)

                # Remaining part is outside the mapping range; go to next mapping
                remaining = map_len - offset
                return self.apply_range(map_src + map_len, remaining, mapped, map_index + 1)


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

# Part 1: lowest location number for seeds
locations = []
for s in seeds:
    l = functools.reduce(lambda x, m: m.apply(x), mappings, s)
    locations.append(l)

print(f"Lowest location number: {min(locations)}")

# Part 2: lowest location number for range of seeds
next_ranges = None
for i, m in enumerate(mappings):
    if i == 0:
        curr_ranges = zip(seeds[0::2], seeds[1::2])
    else:
        curr_ranges = next_ranges

    next_ranges = []
    for start, length in curr_ranges:
        r = m.apply_range(start, length)
        next_ranges.extend(r)

# Sort the ranges by start; first range is lowest location number
sorted_ranges = sorted(next_ranges)
print(f"Lowest location number in ranges: {sorted_ranges[0][0]}")
