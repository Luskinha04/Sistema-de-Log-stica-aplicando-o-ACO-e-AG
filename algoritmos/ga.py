# # algoritmos/ga.py
# import numpy as np
# import random

# def run_ga(
#     matriz_custos,
#     n_pop=50,
#     n_iter=300,
#     p_crossover=0.9,
#     p_mutacao=0.2,
#     elite_frac=0.2,
#     cidade_inicio=0,
#     seed=None
# ):
#     if seed is not None:
#         np.random.seed(seed)
#         random.seed(seed)

#     n_cidades = matriz_custos.shape[0]
#     cidades = list(matriz_custos.index)
#     custos = matriz_custos.values

#     def calc_custo(rota):
#         return sum(custos[rota[i], rota[i + 1]] for i in range(n_cidades)) + custos[rota[-1], rota[0]]

#     pop = []
#     for _ in range(n_pop):
#         rota = list(range(n_cidades))
#         rota.remove(cidade_inicio)
#         random.shuffle(rota)
#         rota = [cidade_inicio] + rota + [cidade_inicio]
#         pop.append(rota)
#     pop = np.array(pop)

#     historico = []
#     melhor_rota = None
#     melhor_custo = float("inf")

#     n_elite = max(1, int(elite_frac * n_pop))

#     # Otimizado: Usar set para deduplicar rotas rapidamente
#     rotas_set = set()
#     top_rotas = []

#     for it in range(n_iter):
#         custos_pop = np.array([calc_custo(ind) for ind in pop])
#         idx_sorted = np.argsort(custos_pop)
#         pop = pop[idx_sorted]

#         # Salvar melhor da geração
#         if custos_pop[idx_sorted[0]] < melhor_custo:
#             melhor_custo = custos_pop[idx_sorted[0]]
#             melhor_rota = pop[0].tolist()
#         historico.append(melhor_custo)

#         # Otimizado: guardar só a elite de cada geração
#         for ind, custo in zip(pop[:n_elite], custos_pop[idx_sorted[:n_elite]]):
#             rota_tupla = tuple(ind)
#             if rota_tupla not in rotas_set:
#                 top_rotas.append((ind.tolist(), custo))
#                 rotas_set.add(rota_tupla)

#         # Elitismo
#         nova_pop = [pop[i].tolist() for i in range(n_elite)]

#         while len(nova_pop) < n_pop:
#             pais = random.sample(list(pop[:20]), 2)
#             if random.random() < p_crossover:
#                 filho = order_crossover(pais[0], pais[1], cidade_inicio)
#             else:
#                 filho = pais[0].tolist()
#             if random.random() < p_mutacao:
#                 filho = mutation(filho, cidade_inicio)
#             nova_pop.append(filho)

#         pop = np.array(nova_pop)

#     # Selecionar as 3 melhores rotas únicas
#     top_rotas = sorted(top_rotas, key=lambda x: x[1])
#     melhores_3 = []
#     rotas_cidades_str = set()
#     for rota_idx, custo in top_rotas:
#         rota_nomes = tuple(cidades[i] for i in rota_idx)
#         if rota_nomes not in rotas_cidades_str:
#             melhores_3.append({"rota": list(rota_nomes), "custo": custo})
#             rotas_cidades_str.add(rota_nomes)
#         if len(melhores_3) == 3:
#             break

#     rota_cidades = [cidades[i] for i in melhor_rota]
#     return {
#         "rota": rota_cidades,
#         "custo": melhor_custo,
#         "historico": historico,
#         "top_3": melhores_3
#     }

# def order_crossover(parent1, parent2, cidade_inicio):
#     n = len(parent1)
#     start, end = sorted(random.sample(range(1, n-1), 2))
#     child = [None] * n
#     child[start:end] = parent1[start:end]
#     pos = end
#     for gene in parent2[1:-1]:
#         if gene not in child:
#             if pos == n-1:
#                 pos = 1
#             child[pos] = gene
#             pos += 1
#     child[0] = parent1[0]
#     child[-1] = parent1[-1]
#     for i in range(1, n-1):
#         if child[i] is None:
#             child[i] = parent2[i]
#     return child

# def mutation(rota, cidade_inicio):
#     n = len(rota)
#     i, j = sorted(random.sample(range(1, n-1), 2))
#     rota[i:j] = reversed(rota[i:j])
#     return rota





import numpy as np
import random

def run_ga(
    matriz_custos,
    matriz_distancias,
    matriz_tempos,
    n_pop=50,
    n_iter=300,
    p_crossover=0.9,
    p_mutacao=0.2,
    elite_frac=0.2,
    cidade_inicio=0,
    seed=None
):
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    n_cidades = matriz_custos.shape[0]
    cidades = list(matriz_custos.index)
    custos = matriz_custos.values
    distancias = matriz_distancias.values
    tempos = matriz_tempos.values

    def calc_custo(rota):
        return sum(custos[rota[i], rota[i + 1]] for i in range(n_cidades)) + custos[rota[-1], rota[0]]

    def calc_distancia(rota):
        return sum(distancias[rota[i], rota[i + 1]] for i in range(n_cidades)) + distancias[rota[-1], rota[0]]

    def calc_tempo(rota):
        return sum(tempos[rota[i], rota[i + 1]] for i in range(n_cidades)) + tempos[rota[-1], rota[0]]

    pop = []
    for _ in range(n_pop):
        rota = list(range(n_cidades))
        rota.remove(cidade_inicio)
        random.shuffle(rota)
        rota = [cidade_inicio] + rota + [cidade_inicio]
        pop.append(rota)
    pop = np.array(pop)

    historico = []
    melhor_rota = None
    melhor_custo = float("inf")
    melhor_dist = float("inf")
    melhor_tempo = float("inf")

    n_elite = max(1, int(elite_frac * n_pop))

    # Otimizado: Usar set para deduplicar rotas rapidamente
    rotas_set = set()
    top_rotas = []

    for it in range(n_iter):
        custos_pop = np.array([calc_custo(ind) for ind in pop])
        dist_pop = np.array([calc_distancia(ind) for ind in pop])
        tempo_pop = np.array([calc_tempo(ind) for ind in pop])
        idx_sorted = np.argsort(custos_pop)
        pop = pop[idx_sorted]

        # Salvar melhor da geração
        if custos_pop[idx_sorted[0]] < melhor_custo:
            melhor_custo = custos_pop[idx_sorted[0]]
            melhor_rota = pop[0].tolist()
            melhor_dist = dist_pop[idx_sorted[0]]
            melhor_tempo = tempo_pop[idx_sorted[0]]
        historico.append(melhor_custo)

        # Guardar só a elite de cada geração
        for ind, custo, dist, tempo in zip(pop[:n_elite], custos_pop[idx_sorted[:n_elite]],
                                           dist_pop[idx_sorted[:n_elite]], tempo_pop[idx_sorted[:n_elite]]):
            rota_tupla = tuple(ind)
            if rota_tupla not in rotas_set:
                top_rotas.append((ind.tolist(), custo, dist, tempo))
                rotas_set.add(rota_tupla)

        # Elitismo
        nova_pop = [pop[i].tolist() for i in range(n_elite)]

        while len(nova_pop) < n_pop:
            pais = random.sample(list(pop[:20]), 2)
            if random.random() < p_crossover:
                filho = order_crossover(pais[0], pais[1], cidade_inicio)
            else:
                filho = pais[0].tolist()
            if random.random() < p_mutacao:
                filho = mutation(filho, cidade_inicio)
            nova_pop.append(filho)

        pop = np.array(nova_pop)

    # Selecionar as 3 melhores rotas únicas
    top_rotas = sorted(top_rotas, key=lambda x: x[1])
    melhores_3 = []
    rotas_cidades_str = set()
    for rota_idx, custo, dist, tempo in top_rotas:
        rota_nomes = tuple(cidades[i] for i in rota_idx)
        if rota_nomes not in rotas_cidades_str:
            melhores_3.append({
                "rota": list(rota_nomes),
                "custo": custo,
                "distancia": dist,
                "tempo": tempo
            })
            rotas_cidades_str.add(rota_nomes)
        if len(melhores_3) == 3:
            break

    rota_cidades = [cidades[i] for i in melhor_rota]
    return {
        "rota": rota_cidades,
        "custo": melhor_custo,
        "distancia": melhor_dist,
        "tempo": melhor_tempo,
        "historico": historico,
        "top_3": melhores_3
    }

def order_crossover(parent1, parent2, cidade_inicio):
    n = len(parent1)
    start, end = sorted(random.sample(range(1, n-1), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    pos = end
    for gene in parent2[1:-1]:
        if gene not in child:
            if pos == n-1:
                pos = 1
            child[pos] = gene
            pos += 1
    child[0] = parent1[0]
    child[-1] = parent1[-1]
    for i in range(1, n-1):
        if child[i] is None:
            child[i] = parent2[i]
    return child

def mutation(rota, cidade_inicio):
    n = len(rota)
    i, j = sorted(random.sample(range(1, n-1), 2))
    rota[i:j] = reversed(rota[i:j])
    return rota
