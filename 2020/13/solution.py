import sys

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

# data = """
# 939
# 7,13,x,x,59,x,31,19
# """

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
