import matplotlib.pyplot as plt
import numpy as np


def load_data(filename: str) -> list:
    with open(filename, 'r') as f:
        return [(int(x), float(y)) for x, y, _ in [line.strip().split(";") for line in f.readlines()]]


def read_all_data(*files: str) -> dict:
    return {file: load_data(file) for file in files}


def plot_data(data: dict, title: str, xlabel: str, ylabel: str, legend: list):
    for key, value in data.items():
        plt.plot(*zip(*value), label=key)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)
    plt.show()

#grafico de colunas com o numero de nos expandidos
def plot_data2(data: dict, title: str, xlabel: str, ylabel: str, legend: list):
    for key, value in data.items():
        plt.bar(*zip(*value), label=key)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)
    plt.show()



def main():
    data = read_all_data("h1.txt", "h2.txt", "h3.txt", "h4.txt", "depth.txt")
    plot_data(data, "Tempo de execução por nível", "Nível", "Tempo (s)",
              ["Heurística 1", "Heurística 2", "Heurística 3", "Heurística 4", "Depth"])

    data = read_all_data("h1.txt", "h2.txt", "h3.txt", "h4.txt")
    plot_data2(data, "Nós expandidos por nível", "Nível", " Número de nós expandidos",
                ["Heurística 1", "Heurística 2", "Heurística 3", "Heurística 4"])


if __name__ == "__main__":
    main()
