import sys
import collections
import functools
import re

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

dataex = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""

# Parse data
robot_descriptor = re.compile(r"Each ([a-z]+) robot costs ([0-9]+) ([a-z]+)(?: and ([0-9]+) ([a-z]+)(?: and )?)*\.")
blueprints = {}
materials = ("ore", "clay", "obsidian", "geode")
for line in data.strip().split('\n'):
    blueprintstr, robotstr = line.split(':')
    blueprint_id = int(blueprintstr[len("Blueprint "):])

    robot_costs = [None, None, None, None]
    robots = robot_descriptor.findall(robotstr)
    for purpose, *costs in robots:
        parsed_costs = {m: int(c) for m, c in zip(costs[1::2], costs[0::2]) if m != ''}
        robot_costs[materials.index(purpose)] = tuple(parsed_costs.get(m, 0) for m in materials)

    blueprints[blueprint_id] = tuple(robot_costs)


# Helper function to determine if a robot can be built with the materials availble
@functools.cache
def can_be_built(have, need):
    return all(h >= n for h, n in zip(have, need))

# Helper function to determine robot build options and impact on collected materials
@functools.cache
def determine_options(materials_collected, robots_available, blueprint):
    # Step 0: determine build options (assume we build one robot at the time)
    robot_build_options = [None] + [i for i, _ in enumerate(materials) if can_be_built(tuple(materials_collected), blueprint[i])]

    # Prioritize
    for i in [0, 1, 2]:
        if robots_available[i] >= max(c[i] for c in blueprint) and i in robot_build_options:
            robot_build_options.remove(i)

    if 4 in robot_build_options or 3 in robot_build_options:
        robot_build_options.remove(None)

    # Process each option as a simulation step (prefer building over not building)
    options = []
    for robot_build_option in robot_build_options[::-1]:
        opt_materials_collected = list(materials_collected)

        # Step 1: take materials for build
        if robot_build_option is not None:
            for i, c in enumerate(blueprint[robot_build_option]):
                opt_materials_collected[i] -= c

        # Step 2: collect materials
        for i, _ in enumerate(materials):
            opt_materials_collected[i] += robots_available[i]

        # Step 3: build robots
        opt_robots_available = list(robots_available)
        if robot_build_option is not None:
            opt_robots_available[robot_build_option] += 1

        options.insert(0, (tuple(opt_materials_collected), tuple(opt_robots_available)))

    return options


# Function to evalute blueprint
def evaluate_blueprint(blueprint):
    t_end = 24
    max_geodes = 0
    initial_materials_collected = (0, 0, 0, 0)
    initial_robots_built = (1, 0, 0, 0)

    to_process = collections.deque()
    to_process.appendleft((0, initial_materials_collected, initial_robots_built))
    seen = set()
    while to_process:
        state = to_process.popleft()
        if state in seen:
            continue
        else:
            seen.add(state)

        t, materials_collected, robots_available = state

        # Determine geodes collected at the end
        if t == t_end:
            if materials_collected[3] > max_geodes:
                max_geodes = materials_collected[3]
                print(max_geodes)
            continue

        geodes_collected = materials_collected[3]
        time_remaining = t_end - t
        potential_geodes_to_collect = robots_available[3] * time_remaining + time_remaining * (time_remaining + 1) // 2
        if geodes_collected + potential_geodes_to_collect < max_geodes:
            continue

        # Determine next step options
        for option in determine_options(materials_collected, robots_available, blueprint):
            opt_materials_collected, opt_robots_available = option
            to_process.appendleft((t + 1, opt_materials_collected, opt_robots_available))

    return max_geodes


# Part 1: sum of quality levels
total = 0
for bpid, blueprint in blueprints.items():
    determine_options.cache_clear()
    q = evaluate_blueprint(blueprint)
    print(can_be_built.cache_info())
    print(determine_options.cache_info())

    print(f"id={bpid}: q={q}")
    total += bpid * q

print(f"Sum of quality levels: {total}")
