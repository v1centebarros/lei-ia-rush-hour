# 97787 103823
"""Example client."""
import asyncio
import getpass
import json
import os
import websockets
from solve import solve, mapping, h, is_goal



async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        boards_cache = []
        moves_cache = []
        prev_board = []


        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                if not boards_cache and not moves_cache:
                    level = state["grid"].split()[1]
                    size_grid = state["dimensions"]
                    print(size_grid)
                    boards_cache = solve(level,h,is_goal,size_grid)
                    prev_board = level

                if not moves_cache:
                    level = state["grid"].split()[1]
                    if prev_board != level:
                        old_mapping = mapping(level,size_grid)
                        def new_heuristic(board):
                            new_mapping = mapping(board,size_grid)
                            return sum(new_mapping[car][0][0] -
                                       old_mapping[car][0][0]
                                       for car in new_mapping)

                        def new_goal(board,size_grid):
                            return board == prev_board

                        new_boards = reversed(solve(level,new_heuristic,new_goal,size_grid))
                        for nb in new_boards:
                            boards_cache.insert(0,nb)

                    board = boards_cache.pop(0)
                    car_mapping = mapping(level,size_grid)
                    new_mapping = mapping(board,size_grid)

                    for car in car_mapping:
                        if car_mapping[car] != new_mapping[car]:
                            vector = new_mapping[car][0][0] - car_mapping[car][0][0], new_mapping[car][0][1] - car_mapping[car][0][1]

                            key = ""
                            if vector[0] > 0:
                                key = "d"
                            elif vector[0] < 0:
                                key = "a"
                            elif vector[1] > 0:
                                key = "s"
                            elif vector[1] < 0:
                                key = "w"

                            if state["selected"] == car and car != level[state["cursor"][1]*6 + state["cursor"][0]]:
                                moves_cache.append((key, board))
                                state["selected"] = ""

                            if state["selected"] == car:
                                moves_cache.append((key, board))
                            else:
                                if state["selected"] != "":
                                    moves_cache.append((" ",state["grid"].split()[1]))


                                pseudo_cursor = state["cursor"]

                                while pseudo_cursor[0] != car_mapping[car][0][0]:
                                    if pseudo_cursor[0] < car_mapping[car][0][0]:
                                        moves_cache.append(("d",state["grid"].split()[1]))
                                        pseudo_cursor[0] += 1
                                    else:
                                        moves_cache.append(("a",state["grid"].split()[1]))
                                        pseudo_cursor[0] -= 1


                                while pseudo_cursor[1] != car_mapping[car][0][1]:
                                    if pseudo_cursor[1] < car_mapping[car][0][1]:
                                        moves_cache.append(("s",state["grid"].split()[1]))
                                        pseudo_cursor[1] += 1
                                    else:
                                        moves_cache.append(("w",state["grid"].split()[1]))
                                        pseudo_cursor[1] -= 1

                                moves_cache.append((" ",state["grid"].split()[1]))
                                moves_cache.append((key,board))

                if moves_cache:
                    key, board = moves_cache.pop(0)
                    prev_board = board
                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )
                # await websocket.send(
                #     json.dumps({"cmd": "key", "key": moves_cache.pop(0)})
                # )


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
