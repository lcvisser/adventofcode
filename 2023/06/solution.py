import sys
import functools
import operator

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Parse data
def parse1(data):
    times_str, distances_str = data.strip().split('\n')
    times = [int(t) for t in times_str[len("Time:"):].strip().split()]
    dists = [int(d) for d in distances_str[len("Distance:"):].strip().split()]
    return times, dists

def parse2(data):
    times_str, distances_str = data.strip().split('\n')
    times = int(times_str.replace(" ", "")[len("Time:"):].strip())
    dists = int(distances_str.replace(" ", "")[len("Distance:"):].strip())
    return [times], [dists]

# Find number of ways to win per race
def number_of_ways_to_win(times, dists):
    n_ways_to_win = []
    for race_time, dist_to_beat in zip(times, dists):
        # Compute distance travelled for each possible velocity
        vel = range(race_time + 1)  # inclusive range
        dist = [v * (race_time - v) for v in vel]  # v == t

        # Find and count the number of times the distance travelled beats the record
        n = len(list(filter(lambda d, D=dist_to_beat: d > D, dist)))
        n_ways_to_win.append(n)

    return n_ways_to_win

# Part 1: multiply the number of ways to win for each race
m1 = functools.reduce(operator.mul, number_of_ways_to_win(*parse1(data)))
print(f"Number of ways to win for all races multiplied: {m1}")

# Part 2: multiply the number of ways to win for one long race
m2 = functools.reduce(operator.mul, number_of_ways_to_win(*parse2(data)))
print(f"Number of ways to win for one race multiplied: {m2}")
