import sys
import collections
import functools
import math
import re

# Read data
input_file = sys.argv[1]
with open(input_file) as f:
    data = f.read()

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


# Enumerated materials
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


# Helper function to determine if a robot can be built with the materials availble
@functools.cache
def can_be_built(have, need):
    return all(h >= n for h, n in zip(have, need))


# Helper function to determine robot build options and impact on collected materials
@functools.cache
def determine_options(materials_collected, robots_available, blueprint):
    # Step 0: determine build options (assume we build one robot at the time); not building is also an option
    robot_build_options = [None] + [i for i in (ORE, CLAY, OBSIDIAN, GEODE) if can_be_built(tuple(materials_collected), blueprint[i])]

    # Prioritize: we can only build one robot per iteration, so if we need at most N material for a particular robot to
    #  build, there is no point in having more than N robots collecting that material
    for i in (ORE, CLAY, OBSIDIAN):
        if robots_available[i] >= max(c[i] for c in blueprint) and i in robot_build_options:
            robot_build_options.remove(i)

    # If we can build geode robot, build it, don't consider not building
    if GEODE in robot_build_options:
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
        for i in (ORE, CLAY, OBSIDIAN, GEODE):
            opt_materials_collected[i] += robots_available[i]

        # Step 3: build robots
        opt_robots_available = list(robots_available)
        if robot_build_option is not None:
            opt_robots_available[robot_build_option] += 1

        options.insert(0, (tuple(opt_materials_collected), tuple(opt_robots_available)))

    return options


# Function to evalute blueprint
def evaluate_blueprint(blueprint, t_end):
    max_geodes = 0
    initial_materials_collected = (0, 0, 0, 0)
    initial_robots_built = (1, 0, 0, 0)

    to_process = collections.deque()
    to_process.appendleft((0, initial_materials_collected, initial_robots_built))
    seen = set()
    while to_process:
        # Keep track of states already processed
        state = to_process.popleft()
        if state in seen:
            continue
        else:
            seen.add(state)

        t, materials_collected, robots_available = state

        # Determine number of geodes collected at the end
        if t == t_end:
            if materials_collected[GEODE] > max_geodes:
                max_geodes = materials_collected[GEODE]
            continue

        # With T minutes remaining, we can collect at most T * num_geode_robots geodes plus T * (T + 1) / 2 additional
        # geodes if we were to build an additional geode robot every iteration (see triangle number); if this potential
        # number of geodes is lower than the maximum already known, abort this path
        geodes_collected = materials_collected[GEODE]
        time_remaining = t_end - t
        potential_geodes_to_collect = time_remaining * robots_available[GEODE] + time_remaining * (time_remaining + 1) // 2
        if geodes_collected + potential_geodes_to_collect < max_geodes:
            # We're not going to catch up, give up this branch
            continue

        # Determine next step options
        for option in determine_options(materials_collected, robots_available, blueprint):
            opt_materials_collected, opt_robots_available = option
            to_process.appendleft((t + 1, opt_materials_collected, opt_robots_available))

    return max_geodes


# Part 1: sum of quality levels
quality_levels = []
for bpid, blueprint in blueprints.items():
    q = evaluate_blueprint(blueprint, 24)
    quality = bpid * q

    print(f"Blueprint id={bpid}: {q} geodes collected (quality={quality})")
    quality_levels.append(quality)

print(f"Sum of quality levels: {sum(quality_levels)}")

# Part 2: total geodes
geodes_collected = []
for bpid in (1, 2, 3):
    q = evaluate_blueprint(blueprints[bpid], 32)

    print(f"Blueprint id={bpid}: {q} geodes collected")
    geodes_collected.append(q)

print(f"Product of geodes collected: {math.prod(geodes_collected)}")
