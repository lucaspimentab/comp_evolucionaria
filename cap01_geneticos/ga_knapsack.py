import time
import numpy as np
import pandas as pd

# Dados
pesos_dos_objetos = np.array([350, 250, 160, 120, 200, 100, 120, 220,  40,  80, 100, 300, 180, 250, 220, 150, 280, 310, 120, 160, 110, 210])
valores_dos_objetos = np.array([300, 400, 450, 350, 250, 300, 200, 250, 150, 400, 350, 300, 450, 500, 350, 400, 200, 300, 250, 300, 150, 200])
capacidade_mochila = 3000
tamanho_do_genoma = len(pesos_dos_objetos)

# Parametros
tamanho_da_populacao = 120
numero_de_geracoes = 300
taxa_de_crossover = 0.9
taxa_de_mutacao = 1.0 / tamanho_do_genoma
tamanho_torneio = 3
usar_elitismo = True

# Funcoes
def calcular_fitness(populacao):
    pesos_totais = np.dot(populacao, pesos_dos_objetos)
    valores_totais = np.dot(populacao, valores_dos_objetos)
    aptidao = np.where(pesos_totais <= capacidade_mochila, valores_totais, 0)
    return aptidao, pesos_totais, valores_totais

def inicializar_populacao():
    return (np.random.randint(0, 2, size=(tamanho_da_populacao, tamanho_do_genoma)))

def selecao_por_torneio(populacao, aptidao):
    indices = np.random.choice(len(populacao), size=tamanho_torneio, replace=False)
    melhor_indice = indices[np.argmax(aptidao[indices])]
    return melhor_indice

def crossover_um_ponto(pai1, pai2):
    if np.random.rand() > taxa_de_crossover:
        return pai1.copy(), pai2.copy()
    ponto = np.random.randint(1, tamanho_do_genoma)
    filho1 = np.concatenate([pai1[:ponto], pai2[ponto:]])
    filho2 = np.concatenate([pai2[:ponto], pai1[ponto:]])
    return filho1, filho2

def mutacao(individuo):
    mascara = (np.random.rand(tamanho_do_genoma) < taxa_de_mutacao)
    individuo_mutado = individuo.copy()
    individuo_mutado[mascara] = 1 - individuo_mutado[mascara]
    return individuo_mutado

# Execucao
inicio = time.time()

populacao = inicializar_populacao()
aptidao, pesos_totais, valores_totais = calcular_fitness(populacao)

melhor_indice = np.argmax(aptidao)
melhor_individuo = populacao[melhor_indice].copy()
melhor_aptidao = int(aptidao[melhor_indice])
melhor_peso = int(pesos_totais[melhor_indice])
melhor_valor = int(valores_totais[melhor_indice])
geracao_do_melhor = 0

for geracao in range(1, numero_de_geracoes + 1):
    nova_populacao = []

    if usar_elitismo:
        nova_populacao.append(melhor_individuo.copy())

    while len(nova_populacao) < tamanho_da_populacao:
        indice_pai1 = selecao_por_torneio(populacao, aptidao)
        indice_pai2 = selecao_por_torneio(populacao, aptidao)
        pai1, pai2 = populacao[indice_pai1], populacao[indice_pai2]

        filho1, filho2 = crossover_um_ponto(pai1, pai2)
        filho1 = mutacao(filho1)
        filho2 = mutacao(filho2)

        nova_populacao.append(filho1)
        if len(nova_populacao) < tamanho_da_populacao:
            nova_populacao.append(filho2)

    populacao = np.array(nova_populacao, dtype=np.int8)
    aptidao, pesos_totais, valores_totais = calcular_fitness(populacao)

    indice_melhor_atual = np.argmax(aptidao)
    if aptidao[indice_melhor_atual] > melhor_aptidao:
        melhor_individuo = populacao[indice_melhor_atual].copy()
        melhor_aptidao = int(aptidao[indice_melhor_atual])
        melhor_peso = int(pesos_totais[indice_melhor_atual])
        melhor_valor = int(valores_totais[indice_melhor_atual])
        geracao_do_melhor = geracao

fim = time.time()
tempo_total = fim - inicio

# Resultados
itens_selecionados = np.where(melhor_individuo == 1)[0] + 1
print("=== Melhor solucao encontrada ===")
print("Itens selecionados:", itens_selecionados.tolist())
print(f"Peso total: {melhor_peso} g (limite {capacidade_mochila} g)")
print(f"Valor total (fitness): {melhor_aptidao}")
print(f"Geracao em que surgiu: {geracao_do_melhor}")
print(f"Tempo de execucao: {tempo_total:.3f} s")

tabela_resultado = pd.DataFrame({
    "Item": np.arange(1, tamanho_do_genoma + 1),
    "Peso (g)": pesos_dos_objetos,
    "Valor": valores_dos_objetos,
    "Selecionado": melhor_individuo.astype(bool)
})
print("\nResumo da solucao:")
print(tabela_resultado[tabela_resultado["Selecionado"]].to_string(index=False))
