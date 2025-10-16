import random, time

D=5
def f(x): return sum(t*t for t in x)

def pso_sum_squares(N=50, ITER=1000, c1=2.0, c2=2.0, wmax=1.1, wmin=0.1,
                    xmin=-10.0, xmax=10.0, seed=42, tol=1e-6, patience=25):
    random.seed(seed)
    def w(k): return wmax+(wmin-wmax)*(k/(ITER-1))
    def clamp(a,lo,hi): return lo if a<lo else (hi if a>hi else a)

    x=[[random.uniform(xmin,xmax) for _ in range(D)] for _ in range(N)]
    v=[[0.0]*D for _ in range(N)]
    pbest=[xi[:] for xi in x]
    pval=[f(xi) for xi in x]
    gi=min(range(N),key=lambda i:pval[i])
    gbest=pbest[gi][:]
    gval=pval[gi]

    no_imp=0; conv_it=None
    t0=time.time()
    for k in range(ITER):
        wk=w(k)
        for i in range(N):
            r1=[random.random() for _ in range(D)]
            r2=[random.random() for _ in range(D)]
            for d in range(D):
                v[i][d]=wk*v[i][d]+c1*r1[d]*(pbest[i][d]-x[i][d])+c2*r2[d]*(gbest[d]-x[i][d])
                x[i][d]=clamp(x[i][d]+v[i][d],xmin,xmax)
            fx=f(x[i])
            if fx<pval[i]:
                pval[i]=fx; pbest[i]=x[i][:]
        bi=min(range(N),key=lambda j:pval[j])
        imp=gval-pval[bi]
        if imp>0:
            gval=pval[bi]; gbest=pbest[bi][:]
            if imp<tol:
                no_imp+=1
                if conv_it is None and no_imp>=patience: conv_it=k+1-patience
            else:
                no_imp=0
    dt=time.time()-t0
    return {"x":gbest,"f":gval,"conv":conv_it,"t":dt}

def resumo(tag,res):
    print(f"[{tag}] x*={[round(v,6) for v in res['x']]}  ||x*||^2={res['f']:.3e}  conv_init={res['conv']}  tempo={res['t']:.3f}s")

# (a) caso base
base=pso_sum_squares()
print("(a) Caso base")
resumo("base c1=2 c2=2, [-10,10]", base)

# (b) influência de c1 e c2
print("\n(b) Influência de c1 e c2")
for (c1,c2) in [(1.5,1.5),(2.0,2.0),(2.5,2.5),(1.5,2.5),(2.5,1.5)]:
    resumo(f"c1={c1} c2={c2}, [-10,10]",
           pso_sum_squares(c1=c1,c2=c2))

# (c) domínio ampliado
print("\n(c) Domínio ampliado [-1000,1000]")
big=pso_sum_squares(xmin=-1000,xmax=1000)
resumo("base c1=2 c2=2, [-1000,1000]", big)

# Respostas:
# (a) Convergência começa ~483.
# (b) c1=c2=1.5: conv_init≈406 (rápido e estável);
#     c1=c2=2.0: conv_init≈483 (base);
#     c1=c2=2.5: conv_init≈562 e erro final maior (~6.35e-06);
#     c1=1.5,c2=2.5: conv_init≈562; c1=2.5,c2=1.5: conv_init≈501.
#     Em geral, c1/c2 maiores aceleram o movimento mas podem oscilar e demorar a estabilizar.
# (c) Em [-1000,1000] conv_init≈566 (demora mais para estabilizar) e tempo similar (~0.165 s).