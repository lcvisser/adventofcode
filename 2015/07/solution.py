with open("2015/07/input.txt") as f:
    data = f.read()


def connect(connections):
    signals = {}

    # Preset constants (for e.g. connections like 1 AND a -> b)
    for i in range(2**16):
        signals[str(i)] = i

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
                # Direct value on wire
                signals[dst] = int(src)
            except ValueError:
                if src in signals.keys():
                    # Direct wire
                    signals[dst] = signals[src]
                else:
                    # Try again later
                    connections.append(connection)

    return signals

connections = data.strip().split("\n")

# Part 1
signals1 = connect(connections.copy())
signal_a1 = signals1["a"] & 0xffff
print(f"Value for wire a: {signal_a1}")

# Part 2
for i, c in enumerate(connections):
    if c.endswith(" -> b"):
        connections[i] = f"{signal_a1} -> b"
        break

signals2 = connect(connections)
signal_a2 = signals2["a"] & 0xffff
print(f"New value for wire a: {signal_a2}")
