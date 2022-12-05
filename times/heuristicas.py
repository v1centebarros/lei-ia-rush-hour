# 97787 103823

# todos os carros * distanica de A ate o final (h4.txt)
def h4(level: str,sizegrid):
    return len(set(level.replace("o","").replace("x",""))) * (sizegrid[0] - (level.index("A") + level.count("A") - 1))

# Pior dos casos (h2) (h3.txt)
def h3(level: str,sizegrid):
    return 2 * (sizegrid[0] - (level.index("A") + level.count("A") - 1))

# heuristic distancia de A ao final + numero de carros bloquear A (h2.txt)
def h2(level: str,sizegrid):
    return sizegrid[0] - (level.index("A") + level.count("A") - 1) + \
           len(level[level.index("A") + level.count("A"):level.index("A")//sizegrid[0]*sizegrid[0] + sizegrid[0]].replace("o",""))

#heuristic distancia de A ao final (h1.txt)
def h1(level: str,sizegrid):
    return sizegrid[0] - (level.index("A") + level.count("A") - 1)