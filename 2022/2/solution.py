import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# A = rock, B = paper, C = scissors
# X = rock, Y = paper, Z = scissors

score_for_shape = {'X': 1, 'Y': 2, 'Z': 3}

def outcome(my_shape, opp_shape):
    played = (my_shape, opp_shape)
    if played in [('X', 'C'), ('Y', 'A'), ('Z', 'B')]:
        # Win
        points = 6
    elif played in [('X', 'A'), ('Y', 'B'), ('Z', 'C')]:
        # Draw
        points = 3
    else:
        # Loss
        points = 0

    return points


# Parse data
lines = data.strip().split('\n')

total_score = 0
for line in lines:
    if line.strip() == '':
        continue

    opp_shape, my_shape = line.strip().split(' ')
    shape_score = score_for_shape[my_shape]
    play_outcome = outcome(my_shape, opp_shape)
    total_score += shape_score + play_outcome

# Part 1:
print(f"Total score: {total_score}")
