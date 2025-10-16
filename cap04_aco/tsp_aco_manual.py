import random, math
import numpy as np

# --- matriz de custos (c_ij)
C = np.array([
    [0,   1.0, 2.2, 2.0, 4.1],
    [1.0, 0,   1.4, 2.2, 4.0],
    [2.2, 1.4, 0,   2.2, 3.2],
    [2.0, 2.2, 2.2, 0,   2.2],
    [4.1, 4.0, 3.2, 2.2, 0.0],
], dtype=float)
N = C.shape[0]

# --- inverso do custo (η_ij = 1/c_ij)
ETA = np.array([
    [0.0,    1.0,   0.454545, 0.5,     0.243902],
    [1.0,    0.0,   0.714286, 0.454545,0.25    ],
    [0.454545,0.714286,0.0,   0.454545,0.3125  ],
    [0.5,    0.454545,0.454545,0.0,   0.454545],
    [0.243902,0.25,  0.3125,  0.454545,0.0     ]
], dtype=float)

# --- feromônio inicial (T_ij)
tau = np.array([
    [0.0, 0.3,  0.25, 0.2,  0.3 ],
    [0.3, 0.0,  0.2,  0.2,  0.3 ],
    [0.25,0.2,  0.0,  0.1,  0.15],
    [0.2, 0.2,  0.1,  0.0,  0.45],
    [0.3, 0.3,  0.15, 0.45, 0.0 ]
], dtype=float)

# --- parâmetros
alpha = 0.5
beta  = 0.5
rho   = 0.5   # evaporação
Q     = 1.0   # depósito
num_ants  = 20
num_iters = 14
rng = random.Random(21)

# --- funções auxiliares
def tour_len(tour):
    L = sum(C[tour[i], tour[i+1]] for i in range(len(tour)-1))
    return L + C[tour[-1], tour[0]]

def constroi_tour():
    start = rng.randrange(N)
    tour = [start]
    nao_visitadas = set(range(N)); nao_visitadas.remove(start)
    atual = start
    while nao_visitadas:
        cand = list(nao_visitadas)
        w = np.array([(tau[atual,j]**alpha)*(ETA[atual,j]**beta) for j in cand], float)
        p = w / w.sum() if w.sum() > 0 else np.ones_like(w)/len(cand)
        r = rng.random()
        idx = int(np.searchsorted(np.cumsum(p), r, side="left"))
        nxt = cand[idx]
        tour.append(nxt); nao_visitadas.remove(nxt); atual = nxt
    return tour

# --- main
best_tour, best_cost = None, math.inf
history = []

for _ in range(num_iters):
    tours, custos = [], []
    for _a in range(num_ants):
        t = constroi_tour()
        c = tour_len(t)
        tours.append(t); custos.append(c)
        if c < best_cost:
            best_cost, best_tour = c, t[:]
    tau *= (1.0 - rho)  # evaporação
    for t, c in zip(tours, custos):  # depósito
        d = Q / c
        for i in range(N):
            a, b = t[i], t[(i+1)%N]
            tau[a,b] += d; tau[b,a] += d
    history.append(best_cost)

print("Histórico do melhor custo:", [float(x) for x in history])
print("Melhor tour (0-based):", best_tour)
print("Melhor custo:", round(best_cost,4))