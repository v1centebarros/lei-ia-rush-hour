# 97787 103823
from collections import defaultdict
import heapq
import functools



def is_goal(level: str, sizegrid):
    return "A" in level[sizegrid[0]-1::sizegrid[0]]


def h(level: str,sizegrid):
    return sizegrid[0] - (level.index("A") + level.count("A") - 1)

def mapping(level: str,sizegrid):
    car_map = defaultdict(list)
    [car_map[level[x + y * sizegrid[0]]].append((x, y)) for x in range(sizegrid[0]) for y in range(sizegrid[1]) if level[x + y * sizegrid[0]] not in ["x","o"]]
    return car_map

#get_neighbours2.0
def get_neighbours(level: str,sizegrid):
    car_map = mapping(level,sizegrid)
    neighbours = []

    for car, _ in car_map.items():
        #vertical
        if(car_map[car][0][0] == car_map[car][-1][0]):
            pos = [(car_map[car][x][0],car_map[car][x][1]-1) for x in range(len(car_map[car]))]
            #UP
            while True:
                if any([y <0 or level[x + y * sizegrid[0]] not in ["o",car] for x,y in pos]):
                    break;
                else:
                    new_level = [("o" if l == car else l) for l in level]

                    new_level[pos[0][0] + pos[0][1] * sizegrid[0]:pos[-1][0] + pos[-1][1] * sizegrid[0] + 1:sizegrid[0] if (pos[0][0] == pos[-1][0]) else 1] = [car for _ in range(len(pos))]

                    neighbours.append("".join(new_level))
                    pos= [(pos[x][0],pos[x][1]-1) for x in range(len(pos))]
            #DOWN
            pos = [(car_map[car][x][0],car_map[car][x][1]+1) for x in range(len(car_map[car]))]
            while True:
                if(any([y >= sizegrid[1] or level[x + y * sizegrid[0]] not in ["o",car] for x,y in pos])):
                    break;
                else:
                    new_level = [("o" if l == car else l) for l in level]

                    new_level[pos[0][0] + pos[0][1] * sizegrid[0]:pos[-1][0] + pos[-1][1] * sizegrid[0] + 1:sizegrid[0] if (pos[0][0] == pos[-1][0]) else 1] = [car for _ in range(len(pos))]

                    neighbours.append("".join(new_level))
                    pos= [(pos[x][0],pos[x][1]+1) for x in range(len(pos))]

        #horizontal
        else:
            pos = [(car_map[car][x][0]-1,car_map[car][x][1]) for x in range(len(car_map[car]))]
            #LEFT
            while True:
                if(any([x <0 or level[x + y * sizegrid[0]] not in ["o",car] for x,y in pos])):
                    break;
                else:
                    new_level = [("o" if l == car else l) for l in level]

                    new_level[pos[0][0] + pos[0][1] * sizegrid[0]:pos[-1][0] + pos[-1][1] * sizegrid[0] + 1:sizegrid[0] if (pos[0][0] == pos[-1][0]) else 1] = [car for _ in range(len(pos))]

                    neighbours.append("".join(new_level))
                    pos= [(pos[x][0]-1,pos[x][1]) for x in range(len(pos))]
            #RIGHT
            pos = [(car_map[car][x][0]+1,car_map[car][x][1]) for x in range(len(car_map[car]))]
            while True:
                if(any([x >= sizegrid[0] or level[x + y * sizegrid[0]] not in ["o",car] for x,y in pos])):
                    break;
                else:
                    new_level = [("o" if l == car else l) for l in level]

                    new_level[pos[0][0] + pos[0][1] * sizegrid[0]:pos[-1][0] + pos[-1][1] * sizegrid[0] + 1:sizegrid[0] if (pos[0][0] == pos[-1][0]) else 1] = [car for _ in range(len(pos))]

                    neighbours.append("".join(new_level))
                    pos= [(pos[x][0]+1,pos[x][1]) for x in range(len(pos))]

    return neighbours


def solve(level: str,heuristic:callable,goal:callable,sizegrid):
    open_set = [level]

    came_from = dict()

    g_score = defaultdict(lambda: float("inf"))
    g_score[level] = 0

    f_score = defaultdict(lambda: float("inf"))
    f_score[level] = heuristic(level,sizegrid)

    while open_set:
        #current = min(open_set, key=lambda x: f_score[x]) #otimizar
        open_set.sort(key=lambda x: f_score[x])
        current = open_set.pop(0)
        if goal(current,sizegrid):
            path = [current]
            while current in came_from.keys():
                current = came_from[current]
                path.insert(0,current)
            return path[1:]

        #open_set.remove(current)
        for neighbour in get_neighbours(current,sizegrid):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbour]:
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = g_score[neighbour] + heuristic(neighbour,sizegrid)
                came_from[neighbour] = current
                if neighbour not in open_set:
                    # printf(new_level)
                    open_set.append(neighbour)

