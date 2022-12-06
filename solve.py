# 97787 103823

from collections import defaultdict, namedtuple
import heapq

Node = namedtuple("Node", ["f_score", "h_score", "g_score", "level", "car_map"])
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
                yield ("".join(new_level), {**level.car_map, car: Position(level.car_map[car].x -1 , level.car_map[car].y, level.car_map[car].size)})


            #RIGHT
            if level.car_map[car].x + level.car_map[car].size -1 < sizegrid[0]-1 and level.level[level.car_map[car].x +level.car_map[car].size + level.car_map[car].y * sizegrid[0]] in ["o",car] :
                new_level = list(level.level)
                new_level[level.car_map[car].x + level.car_map[car].size + level.car_map[car].y * sizegrid[0]] = car
                new_level[level.car_map[car].x + level.car_map[car].y * sizegrid[0]] = "o"
                yield ("".join(new_level), {**level.car_map, car: Position(level.car_map[car].x +1 , level.car_map[car].y, level.car_map[car].size)})
        #vertical
        else:
            #UP
            if level.car_map[car].y > 0 and level.level[level.car_map[car].x + (level.car_map[car].y -1) * sizegrid[0]] in ["o",car]:
                new_level = list(level.level)
                new_level[level.car_map[car].x + (level.car_map[car].y-1) * sizegrid[0]] = car
                new_level[level.car_map[car].x + (level.car_map[car].y + level.car_map[car].size - 1) * sizegrid[0]] = "o"
                yield ("".join(new_level), {**level.car_map, car: Position(level.car_map[car].x , level.car_map[car].y -1, level.car_map[car].size)})


            #DOWN
            if level.car_map[car].y + level.car_map[car].size - 1 < sizegrid[1]-1 and level.level[level.car_map[car].x + (level.car_map[car].y + level.car_map[car].size) * sizegrid[0]] in ["o",car] :
                new_level = list(level.level)
                new_level[level.car_map[car].x + (level.car_map[car].y + level.car_map[car].size) * sizegrid[0]] = car
                new_level[level.car_map[car].x + (level.car_map[car].y) * sizegrid[0]] = "o"
                yield ("".join(new_level), {**level.car_map, car: Position(level.car_map[car].x , level.car_map[car].y +1, level.car_map[car].size)})

def solve(level: str,heuristic:callable,goal:callable,sizegrid):
    open_set = [Node(heuristic(level,sizegrid),heuristic(level,sizegrid), 0,level, mapping(level,sizegrid))]
    came_from = {level: None}
    while open_set:
        current = heapq.heappop(open_set)
        if goal(current.level,sizegrid):
            c = current.level
            path = []
            while c is not None:
                path.insert(0,c)
                c = came_from[c]
            return path[1:]
        for neighbour in get_neighbours(current,sizegrid):
            n = Node(
                heuristic(neighbour[0],sizegrid) + (current.g_score + distancia(current.car_map,neighbour[1])),
                heuristic(neighbour[0],sizegrid),
                current.g_score + 1,
                neighbour[0],
                neighbour[1]
            )
            if n.level not in came_from:
                heapq.heappush(open_set,n)
                came_from[n.level]= current.level

def distancia(car_map1, car_map2):
    return sum (abs(cm1.x - cm2.x) +
                abs(cm1.y - cm2.y) for cm1,cm2 in zip(car_map1.values(),car_map2.values()))


