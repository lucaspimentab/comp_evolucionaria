from random import random

def f(x):
    return (x-4)**2 - (x-8)**3 + 5

# parâmetros
w, c1, c2 = 0.3, 0.7, 0.2
xmin, xmax = 0.0, 15.0

# estado inicial
x = [2.5, 5.6, 10.5]     # p1, p2, p3
v = [0.0, 0.0, 0.0]

# pbest/gbest
pbest = x[:]
pbest_val = [f(xi) for xi in x]
gbest = pbest[pbest_val.index(min(pbest_val))]

# r1,r2 fixos do slide (k=1..6). Cada tupla é (p1),(p2),(p3).
R_fix = [
    [(0.7,0.6),(0.3,0.4),(0.2,0.3)],  # k=1
    [(0.3,0.6),(0.8,0.1),(0.6,0.3)],  # k=2
    [(0.7,0.3),(0.7,0.3),(0.1,0.5)],  # k=3
    [(0.5,0.8),(0.9,0.2),(0.6,0.9)],  # k=4
    [(0.7,0.9),(0.2,0.9),(0.7,0.9)],  # k=5
    [(0.3,0.8),(0.6,0.7),(0.3,0.1)],  # k=6
]

for k in range(14):
    for i in range(3):
        if k < len(R_fix):
            r1, r2 = R_fix[k][i]          # usa os do slide nas 6 primeiras
        else:
            r1, r2 = random(), random()   # segue aleatório

        # atualização PSO
        v[i] = w*v[i] + c1*r1*(pbest[i]-x[i]) + c2*r2*(gbest-x[i])
        x[i] += v[i]

        # domínio [0,15]
        if x[i] < xmin: x[i], v[i] = xmin, 0.0
        if x[i] > xmax: x[i], v[i] = xmax, 0.0

        # atualiza pbest
        fx = f(x[i])
        if fx < pbest_val[i]:
            pbest_val[i], pbest[i] = fx, x[i]

    # atualiza gbest
    gbest = pbest[pbest_val.index(min(pbest_val))]

    # saída enxuta por iteração
    print(f"It {k+1:2d} | x: {[round(xi,2) for xi in x]} | melhor f(x): {min(pbest_val):.2f}")

print(f"\nMelhor solução: x = {gbest:.4f}, f(x) = {min(pbest_val):.4f}")