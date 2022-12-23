import collections
import re


data = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""

robot_descriptor = re.compile(r"Each ([a-z]+) robot costs ([0-9]+) ([a-z]+)(?: and ([0-9]+) ([a-z]+)(?: and )?)*\.")

# Parse data
blueprints = {}

materials = ("ore", "clay", "obsidian", "geode")
RobotCosts = collections.namedtuple("RobotCosts", materials, defaults=[0] * len(materials))

for line in data.strip().split('\n'):
    blueprintstr, robotstr = line.split(':')
    blueprint_id = int(blueprintstr[len("Blueprint "):])

    robot_costs = {}
    robots = robot_descriptor.findall(robotstr)
    for purpose, *costs in robots:
        robot_costs[purpose] = RobotCosts(**{m: int(c) for m, c in zip(costs[1::2], costs[0::2]) if m != ''})

    blueprints[blueprint_id] = robot_costs


robot_costs = blueprints[1]


priorities = ("geode", "obsidian", "clay", "ore")
collected_materials = {m: 0 for m in materials}
robots_built = {m: 0 for m in materials}
robots_built["ore"] = 1
robot_build_queue = []
for i in range(24):
    print(f"Minute {i + 1}: materials: {collected_materials} robots: {robots_built}")
    # Step 1: take materials for build
    for p, collect_material in enumerate(priorities):
        blueprint_costs = robot_costs[collect_material]
        if all(collected_materials[m] >= getattr(blueprint_costs, m) for m in materials):
            # We have the materials; determine if it is desireable to build
            if p == 0:
                # Always build the geode robot as soon as we can
                do_build = True
            else:
                cost_higher_prio_robot = {m: getattr(robot_costs[priorities[p - 1]], m) for m in materials}

                collection_times_needed = {}
                for m in materials:
                    if robots_built[m] == 0:
                        collection_times_needed[m] = float("inf") if cost_higher_prio_robot[m] != 0 else 0
                    else:
                        collection_times_needed[m] = (cost_higher_prio_robot[m] - collected_materials[m]) / robots_built[m]

                time_needed0 = max(collection_times_needed.values())

                collection_times_possible = {}
                for m in materials:
                    if m == collect_material:
                        collection_times_possible[m] = (cost_higher_prio_robot[m] - collected_materials[m]) / (robots_built[m] + 1)
                    else:
                        if robots_built[m] == 0:
                            collection_times_possible[m] = float("inf") if cost_higher_prio_robot[m] != 0 else 0
                        else:
                            collection_times_possible[m] = (cost_higher_prio_robot[m] - collected_materials[m]) / robots_built[m]
                time_needed1 = max(collection_times_possible.values())

                if time_needed1 <= time_needed0:
                    do_build = True
                else:
                    do_build = False

            if do_build:
                for m in materials:
                    collected_materials[m] -= getattr(blueprint_costs, m)
                print(f"Building 1 {collect_material}-collecting robot; materials left: {collected_materials}")
                robot_build_queue.append(collect_material)
                break

    # Collect materials
    for m in materials:
        collected_materials[m] += robots_built[m]
    print(f"Materials after collecting: {collected_materials}")

    # Actual build
    while robot_build_queue:
        r = robot_build_queue.pop(0)
        robots_built[r] += 1
        print(f"Built 1 {r} robot; robots available: {robots_built}")

    print()
    print()