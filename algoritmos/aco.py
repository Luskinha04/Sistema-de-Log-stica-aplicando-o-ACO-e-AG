# # algoritmos/aco.py
# import numpy as np
# import random

# def run_aco(
#     matriz_custos,
#     n_formigas=20,
#     n_iter=300,
#     alfa=1.0,
#     beta=5.0,
#     evaporacao=0.5,
#     feromonio_inicial=1.0,
#     cidade_inicio=0,
#     seed=None
# ):
#     if seed is not None:
#         np.random.seed(seed)
#         random.seed(seed)

#     n_cidades = matriz_custos.shape[0]
#     cidades = list(matriz_custos.index)
#     custos = matriz_custos.values

#     feromonio = np.ones((n_cidades, n_cidades)) * feromonio_inicial
#     visibilidade = 1 / (custos + 1e-10)
#     np.fill_diagonal(visibilidade, 0)

#     melhor_rota = None
#     melhor_custo = float("inf")
#     historico = []

#     # Novo: lista para armazenar as melhores rotas únicas
#     top_rotas = []

#     for iteracao in range(n_iter):
#         rotas = []
#         custos_rotas = []

#         for _ in range(n_formigas):
#             visitado = [False] * n_cidades
#             atual = cidade_inicio
#             caminho = [atual]
#             visitado[atual] = True

#             for _ in range(n_cidades - 1):
#                 probas = []
#                 for j in range(n_cidades):
#                     if not visitado[j]:
#                         prob = (feromonio[atual, j] ** alfa) * (visibilidade[atual, j] ** beta)
#                         probas.append(prob)
#                     else:
#                         probas.append(0)
#                 soma = sum(probas)
#                 if soma == 0:
#                     prox = [j for j, v in enumerate(visitado) if not v][0]
#                 else:
#                     probas = [p / soma for p in probas]
#                     prox = np.random.choice(range(n_cidades), p=probas)
#                 caminho.append(prox)
#                 visitado[prox] = True
#                 atual = prox

#             caminho.append(cidade_inicio)
#             custo_total = sum(custos[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
#             rotas.append(caminho)
#             custos_rotas.append(custo_total)

#             if custo_total < melhor_custo:
#                 melhor_custo = custo_total
#                 melhor_rota = caminho[:]

#         # Atualização de feromônio
#         feromonio = feromonio * (1 - evaporacao)
#         for rota, custo in zip(rotas, custos_rotas):
#             for i in range(len(rota) - 1):
#                 feromonio[rota[i], rota[i + 1]] += 1.0 / (custo + 1e-10)

#         historico.append(melhor_custo)

#         # Guardar todas rotas únicas com custos para análise posterior
#         for rota, custo in zip(rotas, custos_rotas):
#             if (rota, custo) not in top_rotas:
#                 top_rotas.append((rota, custo))

#     # Selecionar as três melhores rotas distintas
#     top_rotas = sorted(top_rotas, key=lambda x: x[1])
#     melhores_3 = []
#     rotas_cidades_str = set()
#     for rota, custo in top_rotas:
#         rota_nomes = tuple(cidades[i] for i in rota)
#         # Checa se a sequência já foi registrada para não duplicar
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









import numpy as np
import random

def run_aco(
    matriz_custos,
    matriz_distancias,
    matriz_tempos,
    n_formigas=20,
    n_iter=300,
    alfa=1.0,
    beta=5.0,
    evaporacao=0.5,
    feromonio_inicial=1.0,
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

    feromonio = np.ones((n_cidades, n_cidades)) * feromonio_inicial
    visibilidade = 1 / (custos + 1e-10)
    np.fill_diagonal(visibilidade, 0)

    melhor_rota = None
    melhor_custo = float("inf")
    melhor_dist = float("inf")
    melhor_tempo = float("inf")
    historico = []

    top_rotas = []

    for iteracao in range(n_iter):
        rotas = []
        custos_rotas = []
        dist_rotas = []
        tempo_rotas = []

        for _ in range(n_formigas):
            visitado = [False] * n_cidades
            atual = cidade_inicio
            caminho = [atual]
            visitado[atual] = True

            for _ in range(n_cidades - 1):
                probas = []
                for j in range(n_cidades):
                    if not visitado[j]:
                        prob = (feromonio[atual, j] ** alfa) * (visibilidade[atual, j] ** beta)
                        probas.append(prob)
                    else:
                        probas.append(0)
                soma = sum(probas)
                if soma == 0:
                    prox = [j for j, v in enumerate(visitado) if not v][0]
                else:
                    probas = [p / soma for p in probas]
                    prox = np.random.choice(range(n_cidades), p=probas)
                caminho.append(prox)
                visitado[prox] = True
                atual = prox

            caminho.append(cidade_inicio)
            custo_total = sum(custos[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
            dist_total = sum(distancias[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
            tempo_total = sum(tempos[caminho[i], caminho[i + 1]] for i in range(len(caminho) - 1))
            rotas.append(caminho)
            custos_rotas.append(custo_total)
            dist_rotas.append(dist_total)
            tempo_rotas.append(tempo_total)

            if custo_total < melhor_custo:
                melhor_custo = custo_total
                melhor_rota = caminho[:]
                melhor_dist = dist_total
                melhor_tempo = tempo_total

        feromonio = feromonio * (1 - evaporacao)
        for rota, custo in zip(rotas, custos_rotas):
            for i in range(len(rota) - 1):
                feromonio[rota[i], rota[i + 1]] += 1.0 / (custo + 1e-10)

        historico.append(melhor_custo)

        for rota, custo, dist, tempo in zip(rotas, custos_rotas, dist_rotas, tempo_rotas):
            if (tuple(rota), custo, dist, tempo) not in top_rotas:
                top_rotas.append((rota, custo, dist, tempo))

    # Selecionar as três melhores rotas distintas
    top_rotas = sorted(top_rotas, key=lambda x: x[1])
    melhores_3 = []
    rotas_cidades_str = set()
    for rota, custo, dist, tempo in top_rotas:
        rota_nomes = tuple(cidades[i] for i in rota)
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
