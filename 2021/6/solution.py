import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# data = "3,4,3,1,2"

# Parse data
initial_fish = [int(x) for x in data.strip().split(',')]

# Simulate (naive implementation)
def simulate(fish, number_of_days):
    for i in range(number_of_days):
        new_fish = 0
        for j in range(len(fish)):
            # Update age
            if fish[j] == 0:
                fish[j] = 6
                new_fish += 1
            else:
                fish[j] -= 1

        # Create new fish
        fish.extend([8] * new_fish)

    return fish

# Simulate long time by cutting timeline into periods
def simulate_by_period(fish, number_of_days, period_length=32):
    # Determine periods to simulate to reach desired number of days
    n_periods, remainder = divmod(number_of_days, period_length)
    periods_to_simulate = [period_length] * n_periods + [remainder]

    # Make a map of the initial number of fish per age
    fish_map = {x: fish.count(x) for x in range(9)}

    for period in periods_to_simulate:
        # Keep track of the new number of fish per age
        fish_map_update = {x: 0 for x in range(9)}

        # Simulate each age for the given period
        for x, n in fish_map.items():
            new_fish = simulate([x], period)

            # Update counters
            for f in new_fish:
                fish_map_update[f] += n

            # Make sure not to count the current age fish twice
            fish_map_update[x] -= n

        # Update the map
        for x, n in fish_map_update.items():
            fish_map[x] += n

    # Count the ttotal number of fish
    return sum(n for n in fish_map.values())


# Part 1
number_of_fish_after_80_days = len(simulate(initial_fish.copy(), 80))
print("Number of fish after 80 days: {}".format(number_of_fish_after_80_days))

# Part 2
number_of_fish_after_256_days = simulate_by_period(initial_fish.copy(), 256)
print("Number of fish after 256 days: {}".format(number_of_fish_after_256_days))
