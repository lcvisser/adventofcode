import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data and score
pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
invalid_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
completion_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
invalid_score = 0
completion_score_per_line = []
for line in data.strip().split('\n'):
    stack = list()
    for c in line:
        if c in pairs.keys():
            # Opening
            stack.append(c)
        else:
            if c == pairs[stack[-1]]:
                # Proper closing
                stack.pop(-1)
            else:
                # Illegal closing
                invalid_score += invalid_scores[c]
                break
    else:
        if stack:
            # Line incomplete
            completion_score = 0
            while stack:
                o = stack.pop()
                c = pairs[o]
                completion_score *= 5
                completion_score += completion_scores[c]
            completion_score_per_line.append(completion_score)

# Part 1: illegal syntax score
print(f"Invalid score: {invalid_score}")

# Part 2: autocompletion score
completion_score_per_line.sort()
number_complete_lines = len(completion_score_per_line)
middle = number_complete_lines // 2
print(f"Autocompletion score: {completion_score_per_line[middle]}")
