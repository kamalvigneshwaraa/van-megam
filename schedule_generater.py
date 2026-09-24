import math

radio_range = 500

nodes = {
    "Node_01": (0, 0),
    "Node_02": (300, 0),
    "Node_03": (600, 0),
    "Node_04": (900, 0),

    "Node_05": (0, 300),
    "Node_06": (300, 300),
    "Node_07": (600, 300),
    "Node_08": (900, 300),

    "Node_09": (0, 600),
    "Node_10": (300, 600),
    "Node_11": (600, 600),
    "Node_12": (900, 600),

    "Node_13": (0, 900),
    "Node_14": (300, 900),
    "Node_15": (600, 900),
    "Node_16": (900, 900)
}


def distance(a, b):
    x1, y1 = a
    x2, y2 = b

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def create_graph():

    graph = {}

    for node in nodes:
        graph[node] = []

    names = list(nodes.keys())

    for i in range(len(names)):

        for j in range(i + 1, len(names)):

            a = names[i]
            b = names[j]

            d = distance(nodes[a], nodes[b])

            if d <= radio_range:
                graph[a].append(b)
                graph[b].append(a)

    return graph


def find_distance(graph, start, end):

    if start == end:
        return 0

    queue = [(start, 0)]
    visited = [start]

    while queue:

        current, level = queue.pop(0)

        for next_node in graph[current]:

            if next_node == end:
                return level + 1

            if next_node not in visited:

                visited.append(next_node)
                queue.append(
                    (next_node, level + 1)
                )

    return None


def create_conflicts(graph):

    conflicts = {}

    for node in graph:
        conflicts[node] = set()

    names = list(graph.keys())

    for i in range(len(names)):

        for j in range(i + 1, len(names)):

            a = names[i]
            b = names[j]

            path = find_distance(graph, a, b)

            if path is not None and path <= 2:

                conflicts[a].add(b)
                conflicts[b].add(a)

    return conflicts


def create_schedule(conflicts):

    order = sorted(
        conflicts,
        key=lambda x: -len(conflicts[x])
    )

    schedule = {}

    for node in order:

        used_slots = []

        for other in conflicts[node]:

            if other in schedule:
                used_slots.append(
                    schedule[other]
                )

        slot = 0

        while slot in used_slots:
            slot += 1

        schedule[node] = slot

    return schedule


def check_schedule(conflicts, schedule):

    wrong = []

    checked = []

    for node in conflicts:

        for other in conflicts[node]:

            pair = tuple(
                sorted([node, other])
            )

            if pair not in checked:

                checked.append(pair)

                if schedule[node] == schedule[other]:
                    wrong.append(pair)

    return wrong


graph = create_graph()

conflicts = create_conflicts(graph)

schedule = create_schedule(conflicts)

wrong = check_schedule(
    conflicts,
    schedule
)


print("=" * 60)
print("TDMA SCHEDULE")
print("=" * 60)

print("Total nodes :", len(nodes))
print("Radio range :", radio_range, "meters")
print()


print("NODE -> SLOT")
print("-" * 60)

for node in sorted(schedule):

    print(
        node,
        "-> Slot",
        schedule[node]
    )


total_slots = max(
    schedule.values()
) + 1

print()
print("Number of slots :", total_slots)


print()
print("SCHEDULE MATRIX")
print("-" * 60)

names = sorted(schedule)

print(
    "Slot |",
    " ".join(
        n.replace("Node_", "")
        for n in names
    )
)

for slot in range(total_slots):

    row = []

    for node in names:

        if schedule[node] == slot:
            row.append("1")
        else:
            row.append("0")

    print(
        f"{slot:4} |",
        " ".join(row)
    )


print()
print("Conflicts checked :",
      sum(len(conflicts[x]) for x in conflicts) // 2)

print("Conflicts found   :",
      len(wrong))

if len(wrong) == 0:
    print("Schedule status   : VALID")
else:
    print("Schedule status   : INVALID")
