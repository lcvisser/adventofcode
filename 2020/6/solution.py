import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

groups = data.split('\n\n')

# Part 1: count number of questions anyone within a group answered with 'yes'
yes_counts = 0
for group in groups:
    yes_questions = set()
    for q in group.replace('\n', ''):
        yes_questions.add(q)
    yes_counts += len(yes_questions)

print(f"Sum of any yes answers: {yes_counts}")

# Part 2: count number of questions everyone within a group answered with 'yes'
yes_counts = 0
for group in groups:
    persons = group.split()
    persons.sort(key=len)
    for q in persons[0]:  # shortest list
        if all(q in p for p in persons):
            yes_counts += 1

print(f"Sum of all yes answers: {yes_counts}")
