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
scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
score = 0
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
                score += scores[c]
                break

# Part 1: illegal syntax score
print(f"Score: {score}")
