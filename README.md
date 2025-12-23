# Computação Evolucionária (Metaheurísticas)

Scripts e notebooks das atividades da disciplina de Metaheurísticas, organizados por capítulo.

## Requisitos
- Python 3.10+
- Dependências em `requirements.txt`

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
```

## Estrutura (resumo)
- `cap01_geneticos/` — GA (mochila)
- `cap04_aco/` — ACO (TSP manual e com `pants`)
- `cap05_pso/` — PSO (exercícios e benchmarks; CSVs/figuras em `data/`)
- `cap06_metaheu/` — SA (agenda) e Tabu/QUBO (rotas)

## Execução
Entre no diretório do capítulo e rode o script desejado:
```bash
cd cap05_pso
python ex1_manual_pso.py
```
