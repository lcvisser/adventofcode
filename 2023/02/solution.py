import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()


MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

# Parse data
possible_games = []
for game in data.strip().split('\n'):
    game_id, reveals = game.split(':')
    game_no = int(game_id[len("Game "):])

    for reveal in reveals.split(';'):
        cubes = reveal.split(',')
        counts = {color: int(count) for count, color in [c.strip().split(' ') for c in cubes]}
        if counts.get("red", 0) > MAX_RED or counts.get("green", 0) > MAX_GREEN or counts.get("blue", 0) > MAX_BLUE:
            break
    else:
        # All reveals possible
        possible_games.append(game_no)

# Part 1: sum of possible game IDs
print(f"Sum of possible game IDs: {sum(possible_games)}")
