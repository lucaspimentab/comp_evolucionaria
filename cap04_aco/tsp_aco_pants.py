import numpy as np
import matplotlib.pyplot as plt
from pants import World, Solver

# matriz de custos
C = np.array([
    [0,   1.0, 2.2, 2.0, 4.1],
    [1.0, 0,   1.4, 2.2, 4.0],
    [2.2, 1.4, 0,   2.2, 3.2],
    [2.0, 2.2, 2.2, 0,   2.2],
    [4.1, 4.0, 3.2, 2.2, 0.0],
])

cities = list(range(len(C)))
def dist(i, j): return float(C[i, j])

world = World(cities, dist)
solver = Solver(limit=200)   # nº de iterações

history = []
best_sol = None
for sol in solver.solutions(world):
    history.append(sol.distance)
    best_sol = sol

if best_sol is not None:
    print("Melhor rota (0-based):", best_sol.tour)
    print("Melhor custo:", round(best_sol.distance, 4))

plt.plot(range(1, len(history)+1), history, marker="o")
plt.xlabel("Iterações")
plt.ylabel("Melhor custo")
plt.title("ACO-Pants no TSP")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("history_pants.png", dpi=160)
plt.show()