import sys

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
import time
from math import prod


# busses = "17,x,13,19"
# busses = "67,7,59,61"
# busses = "67,x,7,59,61"
# busses = "67,7,x,59,61"
# busses = "1789,37,47,1889"

intervals = [int(v) if v != 'x' else -1 for v in busses.split(',')]
offsets = list(range(len(intervals)))
max_interval = max(intervals)
max_offset = offsets[intervals.index(max_interval)]
intervals, offsets = zip(*[(i, o) for i, o in zip(intervals, offsets) if i > 0])

ts1 = max_interval
ts2 = prod(intervals)
match1 = False
match2 = False
t0 = time.monotonic()
n = 0
while not (match1 or match2):
    ts1 += max_interval
    ts2 -= max_interval
    match1 = all(x == 0 for x in [-(ts1 + o - max_offset) % v for v, o in zip(intervals, offsets)])
    match2 = all(x == 0 for x in [-(ts2 + o - max_offset) % v for v, o in zip(intervals, offsets)])
    n += 1

if match1:
    ts = ts1 - max_offset
elif match2:
    ts = ts2 - max_offset
print("First time for all busses: {}".format(ts))
print(time.monotonic() - t0, n, match1, match2)
