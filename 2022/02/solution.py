import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
lines = data.strip().split('\n')

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


def play(opp_shape, goal):
    my_shape_for_goal_and_play = {
        'X': {'A': 'Z', 'B': 'X', 'C': 'Y'},  # loose
        'Y': {'A': 'X', 'B': 'Y', 'C': 'Z'},  # draw
        'Z': {'A': 'Y', 'B': 'Z', 'C': 'X'}  # win
    }
    my_shape = my_shape_for_goal_and_play[goal][opp_shape]
    return my_shape


# Part 1:
total_score = 0
for line in lines:
    if line.strip() == '':
        continue

    opp_shape, my_shape = line.strip().split(' ')
    shape_score = score_for_shape[my_shape]
    play_outcome = outcome(my_shape, opp_shape)
    total_score += shape_score + play_outcome

print(f"Total score: {total_score}")

# Part 2:
total_score = 0
for line in lines:
    if line.strip() == '':
        continue

    opp_shape, goal = line.strip().split(' ')
    my_shape = play(opp_shape, goal)
    shape_score = score_for_shape[my_shape]
    play_outcome = outcome(my_shape, opp_shape)
    total_score += shape_score + play_outcome

print(f"Total score: {total_score}")
