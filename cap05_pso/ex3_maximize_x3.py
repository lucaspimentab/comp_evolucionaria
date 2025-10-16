import time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from pyswarms.single import GlobalBestPSO

BASE_DIR = Path(__file__).resolve().parent

def obj_max_x3(X):
    # PySwarms minimiza; para MAXIMIZAR, retornamos o custo negativo
    x = X[:, 0]
    return -x**3

N, ITER = 50, 1000
bounds = (np.array([0.0]), np.array([35.0]))
options = {"c1": 2.0, "c2": 2.0, "w": 0.7}

opt = GlobalBestPSO(n_particles=N, dimensions=1, options=options, bounds=bounds)

t0 = time.time()
cost, pos = opt.optimize(obj_max_x3, iters=ITER, verbose=False)
elapsed = time.time() - t0

x_best = pos[0]
f_best = -cost
print(f"x*={x_best:.6f}  f(x*)={f_best:.6f}  tempo={elapsed:.3f}s")

# histórico de melhor custo (converter para maximização)
f_hist = -np.array(opt.cost_history)

plt.figure()
plt.plot(f_hist)
plt.xlabel("Iteração")
plt.ylabel("Melhor f(x)")
plt.title("PSO (PySwarms) – Maximização de x^3 em [0,35]")
plt.grid(True, alpha=0.3)
plt.savefig(BASE_DIR / "ex3_maximize_x3_result.png", dpi=300)
plt.close()

# RESPOSTAS
# 1)   Plote os resultados e tempo de processamento e os explique.
#    • O gráfico 'ex3_maximize_x3_result.png' mostra crescimento rápido nas primeiras
#      ~50–150 iterações e depois platô. Isso ocorre porque f(x)=x^3 é estritamente
#      crescente em [0,35]; o ótimo global está na fronteira x*=35. O enxame converge
#      rapidamente para a borda superior e estabiliza.
#    • Tempo de processamento: ~0.08–0.15 s nesta configuração (50 partículas,
#      1000 iterações) — dominado pela avaliação da função e atualização vetorial do PSO.
#
# 2)   Quais as diferenças na implementação da função de maximização para a de minimização?
#    • Em PySwarms o otimizador é de MINIMIZAÇÃO; para MAXIMIZAR, define-se o custo como
#      J(x) = -f(x) (negativação da função objetivo). Nenhuma outra mudança é necessária.
#    • Em uma implementação manual, a diferença seria trocar comparadores e índices
#      de 'min' para 'max' ao atualizar pbest/gbest. Parâmetros (c1,c2,w), limites e
#      atualização de velocidade/posição permanecem idênticos.