# menu/comparacao.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import time
from algoritmos.aco import run_aco
from algoritmos.ga import run_ga
import json
import requests
import polyline
import os

def run_multiple(alg_fn, n, params):
    """Executa o algoritmo n vezes e retorna DataFrame com resultados."""
    resultados = []
    for i in range(n):
        seed = np.random.randint(1, 100000)
        t0 = time.time()
        res = alg_fn(*params, seed=seed)
        t1 = time.time()
        resultados.append({
            "custo": res["custo"],
            "distancia": res["distancia"],
            "tempo_rota": res["tempo"],
            "tempo_execucao": t1 - t0,
            "rota": res["rota"]
        })
    return pd.DataFrame(resultados)

def obter_polyline(origen, destino, coords_dict):
    # Inicializa o cache de polilíneas na sessão, se necessário
    if "polylines_cache" not in st.session_state:
        st.session_state["polylines_cache"] = {}

    cache = st.session_state["polylines_cache"]
    chave = (origen, destino)
    if chave in cache:
        return cache[chave]

    orig_coord = coords_dict[origen]
    dest_coord = coords_dict[destino]

    # Busca a chave da API do Google
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        st.error("Chave da API do Google não configurada.")
        st.stop()

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={orig_coord[0]},{orig_coord[1]}&destination={dest_coord[0]},{dest_coord[1]}"
        f"&key={GOOGLE_API_KEY}"
    )
    resp = requests.get(url)
    data = resp.json()
    if data["status"] == "OK":
        polyline_points = data["routes"][0]["overview_polyline"]["points"]
        coords = polyline.decode(polyline_points)
        cache[chave] = coords
        return coords
    else:
        st.warning(f"Não foi possível obter rota para {origen} → {destino}: {data['status']}")
        return [orig_coord, dest_coord]  # fallback: linha reta

def render():
    st.header("Comparação dos algoritmos")
    st.markdown("Rodar ambos algoritmos várias vezes para avaliar desempenho médio e variabilidade das soluções.")

    # Recupera parâmetros das execuções anteriores
    try:
        aco_params = st.session_state['aco_params']
        ga_params = st.session_state['ga_params']
    except KeyError:
        st.warning("Execute ambos algoritmos pelo menos uma vez para carregar os parâmetros.")
        return

    # Configurações do experimento
    n_execucoes = st.number_input("Número de execuções por algoritmo", 3, 30, 5)

    if st.button("Executar múltiplas simulações"):
        with st.spinner("Executando ACO..."):
            resultados_aco = run_multiple(run_aco, n_execucoes, aco_params)
        with st.spinner("Executando GA..."):
            resultados_ga = run_multiple(run_ga, n_execucoes, ga_params)
        st.session_state['multi_aco'] = resultados_aco
        st.session_state['multi_ga'] = resultados_ga

    # Se já existem execuções múltiplas salvas:
    if ('multi_aco' in st.session_state) and ('multi_ga' in st.session_state):
        resultados_aco = st.session_state['multi_aco']
        resultados_ga = st.session_state['multi_ga']

        st.subheader("Tabela resumo das estatísticas")
        resumo = []
        for nome, df in [("ACO", resultados_aco), ("GA", resultados_ga)]:
            resumo.append({
                "Algoritmo": nome,
                "Custo médio": np.mean(df["custo"]),
                "Custo min": np.min(df["custo"]),
                "Custo max": np.max(df["custo"]),
                "Desvio padrão custo": np.std(df["custo"]),
                "Distância média": np.mean(df["distancia"]),
                "Tempo execução médio (s)": np.mean(df["tempo_execucao"]),
            })
        st.dataframe(pd.DataFrame(resumo).round(2))

        st.subheader("Boxplots comparativos das métricas")
        juntos = pd.concat([
            resultados_aco.assign(Algoritmo="ACO"),
            resultados_ga.assign(Algoritmo="GA")
        ])
        metricas = {
            "Custo": "custo",
            "Distância": "distancia",
            "Tempo execução (s)": "tempo_execucao"
        }
        for label, col in metricas.items():
            fig = px.box(juntos, x="Algoritmo", y=col, points="all", color="Algoritmo", title=f"Boxplot: {label}")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Mapa das melhores rotas encontradas por cada algoritmo")

        # Recupera as melhores rotas (menor custo em todas execuções)
        melhor_aco = resultados_aco.iloc[resultados_aco["custo"].idxmin()]
        melhor_ga = resultados_ga.iloc[resultados_ga["custo"].idxmin()]

        with open("dados/municipios.json", encoding="utf-8") as f:
            dados_cidades = json.load(f)
        coords_dict = {d["nome"]: (d["lat"], d["lng"]) for d in dados_cidades}

        # Checkboxes para mostrar/ocultar cada rota
        col_cb = st.columns(2)
        mostrar_aco = col_cb[0].checkbox("Exibir melhor rota ACO", value=True)
        mostrar_ga  = col_cb[1].checkbox("Exibir melhor rota GA", value=True)

        m = None
        if mostrar_aco or mostrar_ga:
            centro = coords_dict[melhor_aco["rota"][0]]
            m = folium.Map(location=centro, zoom_start=8)
            cidades_marcadas = set()

            if mostrar_aco:
                rota_aco = melhor_aco["rota"]
                rota_real_aco = []
                for i in range(len(rota_aco) - 1):
                    coords_poly = obter_polyline(rota_aco[i], rota_aco[i+1], coords_dict)
                    if i > 0:
                        coords_poly = coords_poly[1:]
                    rota_real_aco.extend(coords_poly)
                folium.PolyLine(rota_real_aco, color="blue", weight=4, tooltip="ACO (melhor)").add_to(m)
                for (lat, lng), nome_cidade in zip([coords_dict[n] for n in rota_aco], rota_aco):
                    if nome_cidade not in cidades_marcadas:
                        folium.CircleMarker(
                            location=[lat, lng], radius=5, color="black",
                            fill=True, fill_color="yellow", fill_opacity=0.7, tooltip=nome_cidade
                        ).add_to(m)
                        cidades_marcadas.add(nome_cidade)

            if mostrar_ga:
                rota_ga = melhor_ga["rota"]
                rota_real_ga = []
                for i in range(len(rota_ga) - 1):
                    coords_poly = obter_polyline(rota_ga[i], rota_ga[i+1], coords_dict)
                    if i > 0:
                        coords_poly = coords_poly[1:]
                    rota_real_ga.extend(coords_poly)
                folium.PolyLine(rota_real_ga, color="purple", weight=4, tooltip="GA (melhor)").add_to(m)
                for (lat, lng), nome_cidade in zip([coords_dict[n] for n in rota_ga], rota_ga):
                    if nome_cidade not in cidades_marcadas:
                        folium.CircleMarker(
                            location=[lat, lng], radius=5, color="black",
                            fill=True, fill_color="yellow", fill_opacity=0.7, tooltip=nome_cidade
                        ).add_to(m)
                        cidades_marcadas.add(nome_cidade)

            st_folium(m, width=800, height=500)
        else:
            st.info("Selecione ao menos uma rota para visualizar o mapa.")

        st.subheader("Conclusão")
        # Conclusão dinâmica
        media_aco = np.mean(resultados_aco["custo"])
        media_ga = np.mean(resultados_ga["custo"])
        dp_aco = np.std(resultados_aco["custo"])
        dp_ga = np.std(resultados_ga["custo"])
        
        melhor_aco_custo = np.min(resultados_aco["custo"])
        melhor_ga_custo = np.min(resultados_ga["custo"])

        if abs(media_aco - media_ga) < 1e-2:
            st.info("Os algoritmos ACO e GA apresentaram desempenhos muito similares em termos de custo médio das rotas para as condições testadas.")
        elif media_aco < media_ga:
            st.info(f"O ACO apresentou menor custo médio ({media_aco:.2f}) em comparação ao GA ({media_ga:.2f}), com desvio padrão {dp_aco:.2f} contra {dp_ga:.2f}.")
        else:
            st.info(f"O GA apresentou menor custo médio ({media_ga:.2f}) em comparação ao ACO ({media_aco:.2f}), com desvio padrão {dp_ga:.2f} contra {dp_aco:.2f}.")

        # Comparação da melhor solução global
        if melhor_aco_custo < melhor_ga_custo:
            st.success(f"A melhor solução global encontrada foi pelo ACO com custo = R$ {melhor_aco_custo:.2f}.")
        elif melhor_ga_custo < melhor_aco_custo:
            st.success(f"A melhor solução global encontrada foi pelo GA com custo = R$ {melhor_ga_custo:.2f}.")
        else:
            st.success("Ambos algoritmos encontraram o mesmo custo mínimo global nas execuções realizadas.")

        st.caption("Observação: Devido ao caráter estocástico, recomenda-se sempre analisar mais de uma execução para conclusões robustas.")
