import sys
from math import prod

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# Part 1: find earliest bus
notes = [x for x in data.split('\n') if len(x) > 0]
ts = notes[0]
busses = notes[1]
bus_ids = [int(v) for v in busses.split(',') if v != 'x']
time_to_wait = [-int(ts) % v for v in bus_ids]
schedule = list(zip(bus_ids, time_to_wait))
schedule.sort(key=lambda x: x[1])
bus = schedule[0]
print("First bus: {} (wait time: {}), number: {}".format(bus[0], bus[1], bus[0] * bus[1]))

# Part 2: find timestamp t so that all busses listed depart at one minute intervals from t
intervals = [int(v) if v != 'x' else -1 for v in busses.split(',')]
offsets = list(range(len(intervals)))
intervals, offsets = zip(*[(i, -o) for i, o in zip(intervals, offsets) if i > 0])

def extended_gcd(a, b):
    """Extended Euclidean algorithm"""
    sp, sc = 1, 0
    tp, tc = 0, 1
    while b > 0:
        a, q, b = b, a // b, a % b
        sp, sc = sc, sp - q * sc
        tp, tc = tc, tp - q * tc

    return a, sp, tp

x = 0
for i in range(len(intervals)):
    N = prod(intervals[:i]) * prod(intervals[i + 1:])
    _, m, M = extended_gcd(intervals[i], N)
    x += offsets[i] * M * N

lcm = prod(intervals)
while x > lcm:
     x -= lcm
print("Timestamp: {}".format(x))
