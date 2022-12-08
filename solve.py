# 97787 103823

from collections import namedtuple
import threading
import heapq

Node = namedtuple("Node", ["f_score", "h_score", "g_score", "level", "car_map", "car_moved","key"])
Position = namedtuple("Position", ["x", "y", "size"])

def is_goal(level: str, sizegrid):
    return "A" in level[sizegrid[0]-1::sizegrid[0]]

def h(level: str,sizegrid):
    return len(set(level.replace("o","").replace("x",""))) * (sizegrid[0] - (level.index("A") + level.count("A") - 1))

def mapping(level: str,sizegrid):
    return {
        car: Position(level.index(car) % sizegrid[0], level.index(car) // sizegrid[0], level.count(car))
        for car in set(level.replace("x", "").replace("o", ""))
    }

def get_neighbours(level,sizegrid):
    for car, _ in level.car_map.items():
        #horizontal
        if level.level[level.car_map[car].x + level.car_map[car].y * sizegrid[0]] == level.level[level.car_map[car].x + 1 + level.car_map[car].y * sizegrid[0]]:
            #LEFT
            if level.car_map[car].x > 0 and level.level[level.car_map[car].x -1 + level.car_map[car].y * sizegrid[0]] in ["o",car] :
                new_level = list(level.level)
                new_level[level.car_map[car].x -1 + level.car_map[car].y * sizegrid[0]] = car
                new_level[level.car_map[car].x + level.car_map[car].size -1 + level.car_map[car].y * sizegrid[0]] = "o"
                yield "".join(new_level), {**level.car_map, car: Position(level.car_map[car].x - 1, level.car_map[car].y, level.car_map[car].size)},car, "a"


            #RIGHT
            if level.car_map[car].x + level.car_map[car].size -1 < sizegrid[0]-1 and level.level[level.car_map[car].x +level.car_map[car].size + level.car_map[car].y * sizegrid[0]] in ["o",car] :
                new_level = list(level.level)
                new_level[level.car_map[car].x + level.car_map[car].size + level.car_map[car].y * sizegrid[0]] = car
                new_level[level.car_map[car].x + level.car_map[car].y * sizegrid[0]] = "o"
                yield "".join(new_level), {**level.car_map, car: Position(level.car_map[car].x + 1, level.car_map[car].y, level.car_map[car].size)},car, "d"
        #vertical
        else:
            #UP
            if level.car_map[car].y > 0 and level.level[level.car_map[car].x + (level.car_map[car].y -1) * sizegrid[0]] in ["o",car]:
                new_level = list(level.level)
                new_level[level.car_map[car].x + (level.car_map[car].y-1) * sizegrid[0]] = car
                new_level[level.car_map[car].x + (level.car_map[car].y + level.car_map[car].size - 1) * sizegrid[0]] = "o"
                yield "".join(new_level), {**level.car_map, car: Position(level.car_map[car].x, level.car_map[car].y - 1, level.car_map[car].size)},car, "w"


            #DOWN
            if level.car_map[car].y + level.car_map[car].size - 1 < sizegrid[1]-1 and level.level[level.car_map[car].x + (level.car_map[car].y + level.car_map[car].size) * sizegrid[0]] in ["o",car] :
                new_level = list(level.level)
                new_level[level.car_map[car].x + (level.car_map[car].y + level.car_map[car].size) * sizegrid[0]] = car
                new_level[level.car_map[car].x + level.car_map[car].y * sizegrid[0]] = "o"
                yield "".join(new_level), {**level.car_map, car: Position(level.car_map[car].x, level.car_map[car].y + 1, level.car_map[car].size)},car, "s"

def solve(level: str,heuristic:callable,goal:callable,sizegrid):
    open_set = [Node(heuristic(level,sizegrid),heuristic(level,sizegrid), 0,level, mapping(level,sizegrid),None,None)]
    came_from = {level: None}
    t = threading.current_thread()
    # non_terminais = 0 
    while open_set and getattr(t, "do_run", True):
        current = heapq.heappop(open_set)
        if goal(current.level,sizegrid):
            c = current
            path = []
            while c is not None:
                path.insert(0,c)
                c = came_from[c.level]
            return path[1:]# , non_terminais
        # non_terminais +=1
        for neighbour in get_neighbours(current,sizegrid):
            n = Node(
                heuristic(neighbour[0],sizegrid) + (current.g_score + distancia(current.car_map,neighbour[1])),
                heuristic(neighbour[0],sizegrid),
                current.g_score + 1,
                *neighbour
            )
            if n.level not in came_from:
                heapq.heappush(open_set,n)
                came_from[n.level]= current


def depth(level:str, goal:callable, sizegrid):
    open_set = [Node(0,0,0,level, mapping(level,sizegrid),None,None)]
    came_from = {level: None}
    t = threading.current_thread()
    while open_set and getattr(t, "do_run", True):
        current = heapq.heappop(open_set)
        if goal(current.level,sizegrid):
            c = current
            path = []
            while c is not None:
                path.insert(0,c)
                c = came_from[c.level]
            return path[1:]
        for neighbour in get_neighbours(current,sizegrid):
            n = Node(
                0,
                0,
                current.g_score + 1,
                *neighbour
            )
            if n.level not in came_from:
                heapq.heappush(open_set,n)
                came_from[n.level]= current

def distancia(car_map1, car_map2):
    return sum (abs(cm1.x - cm2.x) +
                abs(cm1.y - cm2.y) for cm1,cm2 in zip(car_map1.values(), car_map2.values()))
