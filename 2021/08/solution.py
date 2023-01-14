import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
all_patterns = []
all_outputs = []
for line in data.strip().split('\n'):
    pattern_str, output_str = line.split('|')
    pattern = pattern_str.strip().split(' ')
    output = output_str.strip().split(' ')
    all_patterns.append(pattern)
    all_outputs.append(output)

# Part 1: count occurences 1, 4, 7 and 8 in output
count = 0
for output in all_outputs:
    for n in output:
        if len(n) in (2, 4, 3, 7):
            count += 1

print(f"Answer: {count}")

# Part 2: parse and add up
def decode_patterns(patterns):
    # Segment A can be found by comparing the 1 and 7 patterns
    one = list(filter(lambda x: len(x) == 2, patterns))[0]
    seven = list(filter(lambda x: len(x) == 3, patterns))[0]
    segment_A = set(one) ^ set(seven)
    segments_CF = set(one) & set(seven)

    # Segments BD can be found by comparing the 1 and 4 patterns
    four = list(filter(lambda x: len(x) == 4, patterns))[0]
    segments_BD = set(one) ^ set(four)

    # Among 2, 3 and 5, segments B and E are used only once, and A, D and G are used thrice
    two_three_five = list(filter(lambda x: len(x) == 5, patterns))
    counts = {x: 0 for x in "abcdefg"}
    for p in two_three_five:
        for c in p:
            counts[c] += 1
    segments_BE = {c for c, n in counts.items() if n == 1}
    segments_ADG = {c for c, n in counts.items() if n == 3}
    segment_B = segments_BD & segments_BE
    segment_D = segments_BD ^ segment_B
    segment_E = segments_BE ^ segment_B
    segment_G = segments_ADG ^ segment_A ^ segment_D

    # Among 0, 1, 6 and 9, only segment F occurs in all four
    one_zero_nine = list(filter(lambda x: len(x) == 6, patterns))
    segment_F = segments_CF.copy()
    for d in one_zero_nine:
        segment_F &= set(d)
    segment_C = segments_CF ^ segment_F

    # Create mapping (all sets only have one item left)
    mapping = {
        segment_A.pop(): 'A',
        segment_B.pop(): 'B',
        segment_C.pop(): 'C',
        segment_D.pop(): 'D',
        segment_E.pop(): 'E',
        segment_F.pop(): 'F',
        segment_G.pop(): 'G',
    }

    return mapping

def convert_to_number(encoded_segments, mapping):
    segments_to_numbers = {
        "ABCEFG": 0,
        "CF": 1,
        "ACDEG": 2,
        "ACDFG": 3,
        "BCDF": 4,
        "ABDFG": 5,
        "ABDEFG": 6,
        "ACF": 7,
        "ABCDEFG": 8,
        "ABCDFG": 9
    }
    decoded_segments = ''.join(mapping[x] for x in encoded_segments)
    segments = ''.join(sorted(decoded_segments))
    number = segments_to_numbers[segments]
    return number

total = 0
for patterns, outputs in zip(all_patterns, all_outputs):
    segment_mapping = decode_patterns(patterns)
    for i, output in enumerate(outputs):
        number = convert_to_number(output, segment_mapping)
        total += 10**(len(outputs) - i - 1) * number

print(f"Answer: {total}")
