# 97787 103823

from collections import namedtuple, Counter
import threading
import heapq

Node = namedtuple("Node", ["f_score", "h_score", "g_score", "level", "car_map", "car_moved","key"])
Position = namedtuple("Position", ["x", "y", "size"])

def is_goal(level: str, sizegrid):
    """
    :param level: ‘string’ que representa o nível,
    :param sizegrid: dimensões do nível
    :return True se o nível estiver resolvido (se o carro vermelho(A)) esteja enconstado à lateral direita do mapa, False caso contrário
    """
    return "A" in level[sizegrid[0]-1::sizegrid[0]]

def h(level: str,sizegrid):
    """
    :param level: ‘string’ que representa o nível
    :param sizegrid: dimensões do nível
    :return heurística do nível
    """
    return len(set(level.replace("o","").replace("x",""))) * (sizegrid[0] - (level.index("A") + level.count("A") - 1))

def mapping(level: str,sizegrid):
    """
    :param level: ‘string’ que representa o nível,
    :param sizegrid: dimensões do nível,
    :return dicionário de 'Position': dicionário com as coordenadas do canto superior esquerdo de cada carro e o respetivo tamanho
    """
    return {
        car: Position(level.index(car) % sizegrid[0], level.index(car) // sizegrid[0], level.count(car))
        for car in set(level.replace("x", "").replace("o", ""))
    }

def distancia(car_map1, car_map2):
    """
    :param car_map1: dicionário de 'Position'
    :param car_map2: dicionário de 'Position'
    :return Soma da distância de Manhattan entre o carro correspondente dos dicionários de 'Position' dados como argumento
    """
    return sum (abs(cm1.x - cm2.x) +
                abs(cm1.y - cm2.y) for cm1,cm2 in zip(car_map1.values(), car_map2.values()))

def get_neighbours(level,sizegrid):
    """
    :param level: 'Node',
    :param sizegrid: dimensões do nível
    :return iterador sobre um tuplo com a informação dos proximos niveís

    De acordo com cada posição do carro é reescrita a 'string' do 'level' com o avanço ou recuo de cada carro.
    """
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

def a_star(level: str,heuristic:callable,goal:callable,sizegrid):
    """
    :param level: 'string' que representa o nível,
    :param heuristic: função heuristica,
    :param goal: função de verifica se está no objetivo final,
    :param sizegrid: dimensões do nível,
    :return 'path' desde do 'level' até a condicição 'goal' ser True

    Implementação do algoritmo de pesquisa A*
    """
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


def breadth(level:str, goal:callable, sizegrid):
    """
    :param level: 'string' que representa o nível,
    :param goal: função de verifica se está no objetivo final,
    :param sizegrid: dimensões do nível,
    :return 'path' desde do 'level' até a condicição 'goal' ser True

    Implementação do Algoritmo de Pesquisa Grid
    """
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



def simulate(boards, sizegrid, level):
    """
    :param boards: 'path' anteriormente devolvido com solução ao
    :param sizegrid: dimensões do nível,
    :param level: 'string' que representa o nível
    :return None ou uma ação que impede de chegar ao objetivo


    """
    level = list(level)
    for i, move in enumerate(boards):
        position = move.car_map[move.car_moved]
        before = Counter(level)

        if position.x == 0 and move.key == "d":
            return "DROP", i


        if 0 > position.x or sizegrid[0] <= position.x or 0 > position.y or sizegrid[0] <= position.y:
            return "ADD",

        if move.key == "d": # right
            if level[position.y * sizegrid[0] + position.x + position.size - 1] == move.car_moved:
                return "DROP", i
            level[position.y * sizegrid[0] + position.x - 1] = "o"
            level[position.y * sizegrid[0] + position.x + position.size - 1] = move.car_moved
        elif move.key == "a": # left
            if level[position.y * sizegrid[0] + position.x] == move.car_moved:
                return "DROP", i

            level[position.y * sizegrid[0] + position.x + position.size] = "o"
            level[position.y * sizegrid[0] + position.x] = move.car_moved
        elif move.key == "w": # UP
            if level[position.y * sizegrid[0] + position.x + (position.size - 1) * sizegrid[0]] == move.car_moved:
                return "DROP", i
            level[(position.y - 1) * sizegrid[0] + position.x] = "o"
            level[(position.y + position.size - 1) * sizegrid[0] + position.x] = move.car_moved
        elif move.key == "s": # DOWN
            if level[position.y * sizegrid[0] + position.x]  == move.car_moved:
                return "DROP", i
            level[(position.y + position.size) * sizegrid[0] + position.x] = "o"
            level[position.y * sizegrid[0] + position.x] = move.car_moved

        after = Counter(level)
        for (_, v1), (_, v2) in zip(sorted(before.items()), sorted(after.items())):
            if v1 != v2:
                return "ADD",

    if is_goal(level, sizegrid):
        return None
    return "ADD",

