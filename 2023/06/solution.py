import sys
import functools
import operator

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
times_str, distances_str = data.strip().split('\n')
times = [int(t) for t in times_str[len("Time:"):].strip().split()]
dists = [int(d) for d in distances_str[len("Distance:"):].strip().split()]

# Find number of ways to win per race
n_ways_to_win = []
for race_time, dist_to_beat in zip(times, dists):
    # Compute distance travelled for each possible velocity
    vel = range(race_time + 1)  # inclusive range
    dist = [v * (race_time - v) for v in vel]  # v == t

    # Find and count the number of times the distance travelled beats the record
    n = len(list(filter(lambda d, D=dist_to_beat: d > D, dist)))
    n_ways_to_win.append(n)

# Part 1: multiply the number of ways to win for each race
m = functools.reduce(operator.mul, n_ways_to_win)
print(f"Number of ways to win multiplied: {m}")
