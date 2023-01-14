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
    # Step 0: determine build options (assume we build one robot at the time); not building is also an option
    robot_build_options = [None] + [i for i, _ in enumerate(materials) if can_be_built(tuple(materials_collected), blueprint[i])]

    # Prioritize
    if materials.index("geode") in robot_build_options:
        robot_build_options = [materials.index("geode")]
    elif materials.index("obsidian") in robot_build_options:
        robot_build_options = [materials.index("obsidian")]
    else:
        # Ore, clay or not building
        pass

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
    best_geode_collecting = [0] * t_end
    initial_materials_collected = (0, 0, 0, 0)
    initial_robots_built = (1, 0, 0, 0)

    to_process = collections.deque()
    to_process.appendleft((0, initial_materials_collected, initial_robots_built, []))
    while to_process:
        t, materials_collected, robots_available, collected_geodes = to_process.popleft()

        # Determine next step options
        for option in determine_options(materials_collected, robots_available, blueprint):
            opt_materials_collected, opt_robots_available = option
            opt_collected_geodes = collected_geodes.copy()
            opt_collected_geodes.append(opt_materials_collected[materials.index("geode")])

            # Determine geodes collected at the end
            if t + 1 == t_end:
                if opt_collected_geodes[-1] > best_geode_collecting[-1]:
                    best_geode_collecting = opt_collected_geodes.copy()
                    print(best_geode_collecting)
                continue

            # If we're behind, don't continue (we only build one robot per iteration, so we cannot catch up)
            if opt_collected_geodes[t] >= best_geode_collecting[t]:
                to_process.appendleft((t + 1, opt_materials_collected, opt_robots_available, opt_collected_geodes))

    return best_geode_collecting[-1]


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
