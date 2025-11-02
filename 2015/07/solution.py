with open("2015/07/input.txt") as f:
    data = f.read()

signals = {}

# Preset constants (for e.g. connections like 1 AND a -> b)
for i in range(2**16):
    signals[str(i)] = i

connections = data.strip().split("\n")
while connections:
    connection = connections.pop(0)
    src, dst = connection.split(" -> ")

    if "AND" in src:
        inp1, inp2 = src.split(" AND ")
        if inp1 in signals.keys() and inp2 in signals.keys():
            signals[dst] = signals[inp1] & signals[inp2]
        else:
            connections.append(connection)
    elif "OR" in src:
        inp1, inp2 = src.split(" OR ")
        if inp1 in signals.keys() and inp2 in signals.keys():
            signals[dst] = signals[inp1] | signals[inp2]
        else:
            connections.append(connection)
    elif "NOT" in src:
        inp1 = src[len("NOT "):]
        if inp1 in signals.keys():
            signals[dst] = ~signals[inp1]
        else:
            connections.append(connection)
    elif "LSHIFT" in src:
        inp1, s = src.split(" LSHIFT ")
        if inp1 in signals.keys():
            signals[dst] = signals[inp1] << int(s)
        else:
            connections.append(connection)
    elif "RSHIFT" in src:
        inp1, s = src.split(" RSHIFT ")
        if inp1 in signals.keys():
            signals[dst] = signals[inp1] >> int(s)
        else:
            connections.append(connection)
    else:
        try:
            signals[dst] = int(src)
        except ValueError:
            # Direct wire
            if src in signals.keys():
                signals[dst] = signals[src]
            else:
                connections.append(connection)

# Part 1
print(f"Value for wire a: {signals["a"] & 0xffff}")
