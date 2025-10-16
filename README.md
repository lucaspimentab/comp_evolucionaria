# COmputação Evolucionária

Colecao de scripts e notebooks usados nas atividades da disciplina de Metaheuristicas. Cada capitulo concentra os algoritmos, dados auxiliares e artefatos gerados pelas experiencias.

## Preparacao do ambiente
- Utilize Python 3.10 ou superior.
- Crie um ambiente virtual e instale as dependencias de `requirements.txt`:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate  # Windows
  pip install -r requirements.txt
  ```
- O arquivo de requisitos inclui bibliotecas para os diferentes metodos: `numpy`, `pandas`, `matplotlib`, `pyswarms`, `pants`, `simanneal` e o conjunto Ocean da D-Wave (necessario para o TabuSampler).

## Estrutura do repositorio
- `cap01_geneticos/`
  - `ga_knapsack.py`: algoritmo genetico que maximiza o valor acumulado respeitando o limite de 3 kg do problema da mochila. Ao final, imprime o melhor cromossomo e a comparacao de peso.
- `cap04_aco/`
  - `tsp_aco_manual.py`: implementacao manual do Ant Colony Optimization para uma instancia didatica do Problema do Caixeiro Viajante (TSP).
  - `tsp_aco_pants.py`: mesma instancia resolvida com a biblioteca `pants`, gerando o grafico `history_pants.png`.
- `cap05_pso/`
  - `ex1_manual_pso.py`: reproduz as primeiras iteracoes vistas em sala e estende a busca por 14 iteracoes, salvando `data/ex1_iterations.csv`.
  - `ex2_sum_squares_pso.py`: executa o benchmark da soma dos quadrados variando `w`, `c1`, `c2` e limites de busca. Exporta `data/ex2_summary.csv` e `data/ex2_histories.csv`.
  - `ex3_maximize_x3.py`: maximiza `x^3` em `[0, 35]` com `pyswarms`, armazenando a figura `data/ex3_history.png`.
  - `pso_reference_manual.py`: arquivo de apoio mantido para consulta durante as aulas.
- `cap06_metaheu/`
  - `ex1/sa.py`: simulated annealing para montar uma agenda de shows em diferentes cenarios de orcamento, utilizando os CSVs do diretorio e gerando `ex1_summary.csv`.
  - `ex2/ta.py`: formulacao QUBO resolvida com `dwave.samplers.TabuSampler`, encontrando rotas entre estadios brasileiros a partir do Mineirao.

## Saidas geradas
- Arquivos CSV e imagens permanecem no mesmo capitulo onde foram criados, evitando poluir a raiz do projeto.
- Ajuste constantes diretamente nos scripts antes de rodar um experimento especifico.

## Como executar
- Use `python caminho/do/script.py` para disparar cada atividade, por exemplo `python cap05_pso/ex2_sum_squares_pso.py`.
- Para testes com o TabuSampler, garanta que os componentes do Ocean SDK estao instalados e disponiveis no ambiente.
