# 97787 103823

from collections import defaultdict


def is_goal(level: str):
    return "A" in level[5::6]


def h(level: str):
    for i in range(5, -1, -1):
        if "A" in level[i::6]:
            return 5-i
    return float("inf")


def mapping(level: str):
    car_map = defaultdict(list)
    [car_map[level[x + y * 6]].append((x, y)) for x in range(6) for y in range(6) if level[x + y * 6] not in ["x","o"]]
    return car_map


def get_neighbours(level: str):
    car_map = mapping(level)
    neighbours = []

    for car, indexes in car_map.items():
        vector = (indexes[-1][0] - indexes[0][0], indexes[-1][1] - indexes[0][1])
        vector = (
            int(vector[0] / abs(vector[0] + vector[1])),
            int(vector[1] / abs(vector[0] + vector[1])),
        )

        left_or_up = (indexes[0][0] - vector[0], indexes[0][1] - vector[1])
        right_or_down = (indexes[-1][0] + vector[0], indexes[-1][1] + vector[1])
        # print("left_or_up", left_or_up)
        # print("right_or_down", right_or_down)
        if (
                0 <= left_or_up[0] < 6
                and 0 <= left_or_up[1] < 6
                and (level[left_or_up[0] + left_or_up[1] * 6] == "o")
        ):
            new_level = list(level)

            for c in range(len(new_level)):
                if new_level[c] == car:
                    new_level[c] = "o"

            for position in indexes:
                new_level[(position[1] - vector[1]) * 6 + position[0] - vector[0]] = car

            neighbours.append("".join(new_level))

        if (
                0 <= right_or_down[0] < 6
                and 0 <= right_or_down[1] < 6
                and (level[right_or_down[0] + right_or_down[1] * 6] == "o")
        ):
            new_level = list(level)

            for c in range(len(new_level)):
                if new_level[c] == car:
                    new_level[c] = "o"

            for position in indexes:
                new_level[(position[1] + vector[1]) * 6 + position[0] + vector[0]] = car

            neighbours.append("".join(new_level))

    return neighbours


def solve(level: str,heuristic:callable,goal:callable):
    open_set = [level]

    came_from = dict()

    g_score = defaultdict(lambda: float("inf"))
    g_score[level] = 0

    f_score = defaultdict(lambda: float("inf"))
    f_score[level] = h(level)

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if goal(current):
            path = [current]
            while current in came_from.keys():
                current = came_from[current]
                path.insert(0,current)
            return path[1:]

        open_set.remove(current)
        for neighbour in get_neighbours(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbour]:
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = g_score[neighbour] + heuristic(neighbour)
                came_from[neighbour] = current
                if neighbour not in open_set:
                    # print(new_level)
                    open_set.append(neighbour)


