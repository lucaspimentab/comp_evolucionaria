from __future__ import annotations

import os, random, unicodedata
from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, Dict
import numpy as np
import pandas as pd
from simanneal import Annealer

OUTDIR = os.path.join("cap06_metaheu", "ex1")
BUDGET_BASE = 3000
BASE_STEPS = 30_000
RANDOM_SEED = 42  # fixar reprodutibilidade

def _ascii_slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    for ch in r'\/:*?"<>| ':
        s = s.replace(ch, "_")
    return s.lower()

def build_catalog() -> pd.DataFrame:
    return pd.DataFrame({
        "artista": [
            "Taylor Swift","Beyoncé","Tardezinha c/ Thiaguinho","Jorge & Mateus","Anitta",
            "Luísa Sonza","Billie Eilish","Avenged Sevenfold","Nando Reis","Gilberto Gil",
            "Zeca Pagodinho","Joelma","Numanice (Ludmilla)","Adele","Paramore","The Weeknd"
        ],
        "preco":  [1200,1100,300,250,350,280,800,700,200,220,240,180,200,1000,900,950],
        "gosto":  [9.5,9.5,7.0,6.0,6.0,6.5,7.5,6.5,7.5,7.5,7.0,5.5,5.0,8.0,6.5,8.5],
    })

class ShowSelectionAnnealer(Annealer):
    def __init__(self, state: Sequence[int], prices: np.ndarray, tastes: np.ndarray,
                 budget: float, mandatory_indices: Optional[Iterable[int]] = None) -> None:
        self.prices = np.asarray(prices, dtype=float)
        self.tastes = np.asarray(tastes, dtype=float)
        self.budget = float(budget)
        self.mandatory_indices = tuple(mandatory_indices or ())
        super().__init__(list(state))

    def move(self) -> None:
        idxs = list(range(len(self.state)))
        random.shuffle(idxs)
        for i in idxs:
            if i in self.mandatory_indices:
                continue
            self.state[i] = 1 - self.state[i]
            return

    def energy(self) -> float:
        s = np.asarray(self.state, dtype=float)
        cost  = float(s @ self.prices)
        taste = float(s @ self.tastes)
        count = int(s.sum())
        pen = 0.0
        if cost > self.budget:
            pen += 1000.0 * (cost - self.budget)
        missing = sum(1 for i in self.mandatory_indices if self.state[i] == 0)
        if missing:
            pen += 5000.0 * missing
        return -(1000.0 * count + taste) + pen  # minimizar energia == maximizar (#shows, gosto)

@dataclass
class ScenarioResult:
    label: str
    budget: float
    mandatory: tuple[str, ...]
    state: np.ndarray
    selection: pd.DataFrame
    nshows: int
    cost: float
    taste: float
    energy: float

def run_sa(df: pd.DataFrame, *, budget: float, mandatory_artists: Iterable[str] = (),
           steps: int = BASE_STEPS, seed: Optional[int] = RANDOM_SEED) -> ScenarioResult:
    if seed is not None:
        random.seed(seed); np.random.seed(seed)
    mand = tuple(mandatory_artists or ())
    mand_idx = tuple(df.index[df["artista"] == a][0] for a in mand) if mand else ()
    init = np.zeros(len(df), dtype=int)
    for i in mand_idx:
        init[i] = 1
    sa = ShowSelectionAnnealer(init, df["preco"].to_numpy(), df["gosto"].to_numpy(), budget, mand_idx)
    sa.steps = steps; sa.copy_strategy = "deepcopy"; sa.updates = 0
    best_state, best_E = sa.anneal()
    best_state = np.asarray(best_state, dtype=int)
    sel = df[best_state.astype(bool)].copy().sort_values("gosto", ascending=False)
    return ScenarioResult(
        label="", budget=float(budget), mandatory=mand, state=best_state,
        selection=sel, nshows=int(sel.shape[0]), cost=float(sel["preco"].sum()),
        taste=float(sel["gosto"].sum()), energy=float(best_E)
    )

def write_items_csv(label: str, r: ScenarioResult) -> str:
    os.makedirs(OUTDIR, exist_ok=True)
    t = r.selection[["artista","preco","gosto"]].copy()
    t["gosto_por_real"] = t["gosto"] / t["preco"]
    t.loc["TOTAL", ["artista","preco","gosto","gosto_por_real"]] = [
        f"— {r.nshows} shows —", int(r.cost), r.taste, t["gosto_por_real"].mean()
    ]
    path = os.path.join(OUTDIR, f"{_ascii_slug(label)}_itens.csv")
    t.to_csv(path, encoding="utf-8")
    return path

def write_summary_csv(results: Dict[str, ScenarioResult], base_key: str = "BASE") -> str:
    rows = []
    base = results[base_key]
    for k, r in results.items():
        rows.append({
            "cenario": k,
            "orcamento": r.budget,
            "n_shows": r.nshows,
            "custo": int(r.cost),
            "gosto": r.taste,
            "delta_shows_vs_BASE": r.nshows - base.nshows,
            "delta_custo_vs_BASE": r.cost - base.cost,
            "delta_gosto_vs_BASE": r.taste - base.taste,
        })
    df = pd.DataFrame(rows).sort_values("cenario")
    path = os.path.join(OUTDIR, "ex1_summary.csv")
    df.to_csv(path, index=False, float_format="%.2f", encoding="utf-8")
    return path

def summarize(r: ScenarioResult) -> str:
    nomes = ", ".join(r.selection["artista"].tolist())
    return f"{r.label}: {r.nshows} shows | R$ {int(r.cost)} | gosto={r.taste:.1f} | {nomes}"

def main() -> None:
    df = build_catalog()

    base = run_sa(df, budget=BUDGET_BASE, steps=BASE_STEPS); base.label = "BASE"

    # OU: força Taylor e Beyoncé separadamente e escolhe o melhor por (n_shows, gosto)
    r_t = run_sa(df, budget=BUDGET_BASE, mandatory_artists=("Taylor Swift",), steps=BASE_STEPS)
    r_b = run_sa(df, budget=BUDGET_BASE, mandatory_artists=("Beyoncé",),      steps=BASE_STEPS)
    best_ou = r_t if (r_t.nshows, r_t.taste) >= (r_b.nshows, r_b.taste) else r_b
    best_ou.label = "MAND_TAYLOR_OR_BEYONCE"

    s2600 = run_sa(df, budget=2600, steps=25_000); s2600.label = "BUDGET_2600"
    s3200 = run_sa(df, budget=3200, steps=35_000); s3200.label = "BUDGET_3200"

    results = {r.label: r for r in [base, best_ou, s2600, s3200]}
    for r in results.values():
        print(summarize(r))

    for key, r in results.items():
        write_items_csv(key, r)
    write_summary_csv(results, base_key="BASE")

if __name__ == "__main__":
    main()

# (a) Restrição "Taylor OU Beyoncé": rodamos dois SA (forçando Taylor e forçando Beyoncé)
#     e escolhemos o melhor por (n_shows, gosto). Ex.: BASE = 10 shows | R$ 2920 | gosto 64.5;
#     MAND_TAYLOR_OR_BEYONCE = 9 shows | R$ 2970 | gosto 61.5 → Δshows = −1; Δcusto = +R$ 50; Δgosto = −3.0.
# (b) Sensibilidade: com R$ 2600 → 9 shows | R$ 2570 | gosto 58.5 (queda vs BASE);
#     com R$ 3200 → 10 shows | R$ 3170 | gosto 66.5 (mantém nº máximo e aumenta o gosto).