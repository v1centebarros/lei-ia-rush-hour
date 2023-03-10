# 97787 103823


"""Example client."""
import asyncio
import getpass
import json
import os
import websockets
import threading
from solve import a_star, mapping, is_goal, breadth, h

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        boards_cache = []
        moves_cache = []
        prev_board = []
        current_level = ""

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                # Caso não tenha nada ou o nível tenha mudado recalcular
                if (not boards_cache and not moves_cache) or current_level != state["level"]:
                    level = state["grid"].split()[1] # string de level
                    size_grid = state["dimensions"]  # tuplo de dimensões

                    #Verificar qual é o melhor algoritmo a usar para obter o melhor resultado
                    if size_grid[0] <= 6:
                        boards_cache = breadth(level, is_goal, size_grid)
                    else:
                        boards_cache = a_star(level,h,is_goal,size_grid)

                    # O nível anterior é o nível atual
                    prev_board = level
                    current_level = state["level"]
                    moves_cache = []


                if not moves_cache and boards_cache:
                    level = state["grid"].split()[1]
                    if prev_board != level: #and simulate(boards_cache, size_grid, level) is not None: #Usar o simulate para verificar para prever os crazy cars

                        # Lidar com os crazy cars
                        LIMIT = 1 / (state["game_speed"] * 2)

                        def wrapper(out, level,h,is_goal,size_grid):

                            if size_grid[0] <= 6:
                                out.append(breadth(level, is_goal, size_grid))
                            else:
                                out.append(a_star(level,h,is_goal,size_grid))
                        res = []
                        t = threading.Thread(target=wrapper, args=(res, level,h,is_goal,size_grid))
                        t.start()
                        t.join(LIMIT)
                        if t.is_alive():
                            t.do_run = False
                            old_mapping = mapping(prev_board,size_grid)
                            def new_heuristic(board,size_grid):
                                new_mapping = mapping(board,size_grid)
                                #distancia manhattan
                                return sum(abs(old_mapping[car].x -
                                               new_mapping[car].x) + \
                                           abs(old_mapping[car].y -
                                               new_mapping[car].y) for car in new_mapping)

                            def new_goal(board,size_grid):
                                return board == prev_board

                            if size_grid[0] <= 6:
                                new_boards = breadth(level, new_goal, size_grid)
                            else:
                                new_boards = a_star(level,new_heuristic,new_goal,size_grid)

                            boards_cache = new_boards + boards_cache
                        else:
                            boards_cache = res[0] + boards_cache

                    # Fazer o movimento
                    if boards_cache:
                        board = boards_cache.pop(0)
                        car_mapping = mapping(level, size_grid)
                        new_mapping = mapping(board.level, size_grid)

                        key = ""
                        for car in car_mapping:
                            if car_mapping[car] != new_mapping[car]:
                                vector = new_mapping[car].x - car_mapping[car].x, new_mapping[car].y - car_mapping[car].y
                                if vector[0] > 0:
                                    key = "d"
                                elif vector[0] < 0:
                                    key = "a"
                                elif vector[1] > 0:
                                    key = "s"
                                elif vector[1] < 0:
                                    key = "w"
                                break

                        # carro selecionado certo
                        if state["selected"] == car:
                            moves_cache.append((key, board.level))
                        # nenhum carro selecionado
                        else:
                            if state["selected"] != "":
                                moves_cache.append((" ", board.level))

                            direction = "H" if level[car_mapping[car].x + car_mapping[car].y * size_grid[0]] == level[car_mapping[car].x + 1 + car_mapping[car].y * size_grid[0]] else "V"
                            pseudo_cursor = state["cursor"]

                            while  not (car_mapping[car].x <= pseudo_cursor[0] <= car_mapping[car].x + (car_mapping[car].size-1) * (direction == "H")):
                                if pseudo_cursor[0] < car_mapping[car].x:
                                    moves_cache.append(("d", state["grid"].split()[1]))
                                    pseudo_cursor[0] += 1
                                else:
                                    moves_cache.append(("a", state["grid"].split()[1]))
                                    pseudo_cursor[0] -= 1


                            while not (car_mapping[car].y <= pseudo_cursor[1] <= car_mapping[car].y + (car_mapping[car].size-1) * (direction == "V")):
                                if pseudo_cursor[1] < car_mapping[car].y:
                                    moves_cache.append(("s", state["grid"].split()[1]))
                                    pseudo_cursor[1] += 1
                                else:
                                    moves_cache.append(("w", state["grid"].split()[1]))
                                    pseudo_cursor[1] -= 1

                            moves_cache.append((" ", level))
                            moves_cache.append((key, board.level))

                if moves_cache:
                    key, board = moves_cache.pop(0)
                    prev_board = board
                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )


            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))

