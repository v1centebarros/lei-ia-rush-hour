import time
import math

from solve import a_star, is_goal
from times.heuristicas import h1, h2, h3, h4



def level_times(h,file_name):
    levels = open("levels.txt", "r").read().split("\n")
    f = open(file_name, "w")
    start = time.time()
    i = 1 
    for level in levels:
        start = time.time()
        if not level:
            continue
        level = level.split(" ")[1]
        size = int(math.sqrt(len(level)))
        x = a_star(level, h, is_goal, (size,size))
        print(f"SOLUTION LENGTH: { i, len(x)}")
        f.write(f"{i};{time.time()-start};{len(x)}\n")
        i += 1
        
    print("DONE")
    
def level_no_expandidos(h,file_name):
    levels = open("levels.txt", "r").read().split("\n")
    f = open(file_name, "w")
    start = time.time()
    i = 1 
    for level in levels:
        start = time.time()
        if not level:
            continue
        level = level.split(" ")[1]
        size = int(math.sqrt(len(level)))
        x = a_star(level, h, is_goal, (size,size))
        print(f"SOLUTION LENGTH: { i, len(x[0]), x[1]}")
        f.write(f"{i};{x[1]};{len(x[0])}\n")
        i += 1
        
    print("DONE")

if __name__ == "__main__":
    level_times(h1, "times/h1.txt")
    level_times(h2, "times/h2.txt")
    level_times(h3, "times/h3.txt")
    level_times(h4, "times/h4.txt")

    level_no_expandidos(h1, "times/h1_no.txt")
    level_no_expandidos(h2, "times/h2_no.txt")
    level_no_expandidos(h3, "times/h3_no.txt")
    level_no_expandidos(h4, "times/h4_no.txt")

