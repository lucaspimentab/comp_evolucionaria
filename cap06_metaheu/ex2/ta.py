from collections import defaultdict
from dwave.samplers import TabuSampler


stadiums = [
    "Mineirão (Belo Horizonte)","Maracanã (Rio de Janeiro)","Morumbi (São Paulo)","Mané Garrincha (Brasília)",
    "Beira-Rio (Porto Alegre)","Arena da Baixada (Curitiba)","Arena Fonte Nova (Salvador)","Castelão (Fortaleza)",
    "Arena Pernambuco (Recife)","Mangueirão (Belém)","Arena Pantanal (Cuiabá)","Serra Dourada (Goiânia)"
]
dist = [
 [0,434,629,770,1686,1032,1202,2351,2039,2640,1714,822],
 [434,0,456,1165,1406,844,1515,2730,2340,3074,1971,1166],
 [629,456,0,1098,1059,412,1830,2962,2666,3098,1658,1014],
 [770,1165,1098,0,2030,1355,1324,2101,2056,2004,1100,219],
 [1686,1406,1059,2030,0,685,2885,4014,3720,4004,2105,1875],
 [1032,844,412,1355,685,0,2234,3332,3070,3348,1632,1216],
 [1202,1515,1830,1324,2885,2234,0,1275,836,2115,2400,1531],
 [2351,2730,2962,2101,4014,3332,1275,0,762,1419,2911,2312],
 [2039,2340,2666,2056,3720,3070,836,762,0,2078,3056,2274],
 [2640,3074,3098,2004,4004,3348,2115,1419,2078,0,2240,2132],
 [1714,1971,1658,1100,2105,1632,2400,2911,3056,2240,0,932],
 [822,1166,1014,219,1875,1216,1531,2312,2274,2132,932,0],
]
N, START = len(stadiums), 0
v = lambda i,p: f"x_{i}_{p}"

def rotate_to_start(route, start=START):
    k = route.index(start); return route[k:]+route[:k]

def route_cost(route):
    return sum(dist[a][b] for a,b in zip(route,route[1:])) + dist[route[-1]][route[0]]

def build_qubo(A=6000.0, B=1.0, Afix=6000.0):
    Q = defaultdict(float)
    # 1) cada posição p tem 1 cidade
    for p in range(N):
        for i in range(N): Q[(v(i,p),v(i,p))] += -A
        for i in range(N):
            for j in range(i+1,N): Q[(v(i,p),v(j,p))] += 2*A
    # 2) cada cidade i aparece 1 vez
    for i in range(N):
        for p in range(N): Q[(v(i,p),v(i,p))] += -A
        for p in range(N):
            for q in range(p+1,N): Q[(v(i,p),v(i,q))] += 2*A
    # 3) custo do percurso p->p+1 (ciclo)
    for p in range(N):
        q = (p+1) % N
        for i in range(N):
            for j in range(N):
                if i!=j: Q[(v(i,p),v(j,q))] += B*dist[i][j]
    # 4) fixa Mineirão na posição 0
    Q[(v(START,0),v(START,0))] += -Afix
    return Q

def solve_tabu(params):
    Q = build_qubo(**{k:params[k] for k in ("A","B","Afix")})
    sampler = TabuSampler()
    resp = sampler.sample_qubo(Q, num_reads=params["reads"], timeout=params["timeout"])
    sample = resp.first.sample
    # decodifica (cidade na posição p)
    pos_to_city = [max(range(N), key=lambda i: sample.get(v(i,p),0)) for p in range(N)]
    route = rotate_to_start(pos_to_city, START)
    return route, route_cost(route)

def print_route(route, cost, tag):
    print(f"\n=== {tag} ===")
    for i in route: print(stadiums[i])
    print(f"Distância total (km): {cost:.1f}")

# Experimentos (PARTE B)
base =  {"A":6000.0,"B":1.0,"Afix":6000.0,"timeout":2000,"reads":40}
alt  =  {"A":7000.0,"B":1.0,"Afix":7000.0,"timeout":3500,"reads":80}  # mais “duro” e mais intensivo

r1,c1 = solve_tabu(base); print_route(r1,c1,"Configuração A (base)")
r2,c2 = solve_tabu(alt);  print_route(r2,c2,"Configuração B (mais penalidade + mais tempo)")

# (a) Rota e distância — TSP dos estádios (início/fim: Mineirão)
#     Config A (base): Mineirão → Arena Fonte Nova → Arena Pernambuco → Castelão → Mangueirão → Mané Garrincha → Serra Dourada → Arena Pantanal → Beira-Rio → Arena da Baixada → Morumbi → Maracanã | 11 466,0 km
#     Config B (penalidade+tempo↑): Mineirão → Maracanã → Morumbi → Arena da Baixada → Beira-Rio → Arena Pantanal → Serra Dourada → Mané Garrincha → Mangueirão → Castelão → Arena Pernambuco → Arena Fonte Nova | 11 466,0 km
#     Observação: As rotas são diferentes, mas a distância total é a mesma. Escolha indiferente do ponto de vista de custo.

# (b) Sensibilidade (efeito de parâmetros)
#     Aumento de penalidade/tempo (B) NÃO alterou o custo total (Δdist = 0,0 km), apenas a ordem da rota.
#     Interpretação: existem múltiplas soluções ótimas/empatadas para este TSP; a Busca Tabu pode retornar ciclos distintos com mesma qualidade.
#     Conclusão: solução robusta em termos de custo; ajustes de intensificação influenciam a rota escolhida, mas não a qualidade final nesta instância.
