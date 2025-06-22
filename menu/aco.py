# menu/aco.py
import streamlit as st
import pandas as pd
from algoritmos.aco import run_aco
import folium
from streamlit_folium import st_folium
import json
import os
import plotly.graph_objects as go
import time
import requests
import polyline
from dotenv import load_dotenv

def render():
    st.header("Algoritmo de colônia de formigas (ACO)")

    matriz_custos = pd.read_csv("dados/matriz_custos.csv", index_col=0)
    matriz_distancias = pd.read_csv("dados/matriz_distancias.csv", index_col=0)
    matriz_tempos = pd.read_csv("dados/matriz_tempos.csv", index_col=0)
    cidades = matriz_custos.index.tolist()

    idx_patrocinio = cidades.index("Patrocínio") if "Patrocínio" in cidades else 0
    cidade_inicio = st.selectbox("Cidade inicial/final", cidades, index=idx_patrocinio)

    st.subheader("Parâmetros do ACO")
    n_formigas = st.number_input("Número de formigas", 1, 100, 20)
    n_iter = st.number_input("Número de iterações", 10, 10000, st.session_state.get("max_iter", 1000), step=10)
    alfa = st.slider("Alfa (peso do feromônio)", 0.1, 5.0, 1.0, 0.1)
    beta = st.slider("Beta (peso da heurística)", 0.1, 10.0, 5.0, 0.1)
    evaporacao = st.slider("Taxa de evaporação", 0.01, 1.0, 0.5, 0.01)

    # Inicializar cache de polilíneas
    if "polylines_cache" not in st.session_state:
        st.session_state["polylines_cache"] = {}

    # Clave de Google API (reemplaza con tu método de cargar claves si es necesario)
    load_dotenv()
    # GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        st.error("No hay clave de Google API configurada.")
        return

    # Función para obtener la polyline real entre dos ciudades (cacheada)
    def obtener_polyline(origen, destino, coords_dict):
        cache = st.session_state["polylines_cache"]
        clave = (origen, destino)
        if clave in cache:
            return cache[clave]
        orig_coord = coords_dict[origen]
        dest_coord = coords_dict[destino]
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
            cache[clave] = coords
            return coords
        else:
            st.warning(f"No se pudo obtener ruta para {origen} → {destino}: {data['status']}")
            return [orig_coord, dest_coord]  # fallback recto

    if st.button("Executar ACO"):
        idx_inicio = cidades.index(cidade_inicio)
        t0 = time.time()
        resultado = run_aco(
            matriz_custos,
            matriz_distancias,
            matriz_tempos,
            n_formigas=n_formigas,
            n_iter=n_iter,
            alfa=alfa,
            beta=beta,
            evaporacao=evaporacao,
            cidade_inicio=idx_inicio
        )
        t1 = time.time()

        st.session_state["aco_params"] = [
            matriz_custos,
            matriz_distancias,
            matriz_tempos,
            int(n_formigas),
            int(n_iter),
            float(alfa),
            float(beta),
            float(evaporacao),
            idx_inicio
        ]

        resultado["tempo_execucao"] = t1 - t0
        st.session_state["aco_resultado"] = resultado
        st.session_state["aco_resultados_comparativo"] = {
            "rota": resultado["rota"],
            "custo": resultado["custo"],
            "distancia": resultado["distancia"],
            "tempo": resultado["tempo"],
            "historico": resultado["historico"],
            "top_3": resultado["top_3"],
            "tempo_execucao": resultado["tempo_execucao"]
        }

    if "aco_resultado" in st.session_state:
        resultado = st.session_state["aco_resultado"]
        st.success(f"Melhor rota encontrada: {' → '.join(resultado['rota'])}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<span style="font-size:1.35rem;font-weight:600;color:#000000">R$ {resultado["custo"]:.2f}</span><br><span style="font-size:0.9rem;">Custo total</span>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f'<span style="font-size:1.35rem;font-weight:600;color:#000000">{resultado["distancia"]:.2f} km</span><br><span style="font-size:0.9rem;">Distância total</span>',
                unsafe_allow_html=True
            )
        with col3:
            horas = resultado["tempo"] / 60.0
            st.markdown(
                f'<span style="font-size:1.35rem;font-weight:600;color:#000000">{horas:.2f} h</span><br><span style="font-size:0.9rem;">Tempo total</span>',
                unsafe_allow_html=True
            )

        with open("dados/municipios.json", encoding="utf-8") as f:
            dados_cidades = json.load(f)
        coords_dict = {d["nome"]: (d["lat"], d["lng"]) for d in dados_cidades}

        cores = ["blue", "red", "orange"]
        cores_emojis = ["🔵", "🔴", "🟠"]

        colunas = st.columns(3)
        mostrar_rotas = []
        for idx, rota_info in enumerate(resultado.get("top_3", [])):
            checked = True if idx == 0 else False
            label = f"{cores_emojis[idx]} Rota #{idx+1} (Custo: R$ {rota_info['custo']:.2f})"
            with colunas[idx]:
                mostrar = st.checkbox(label, value=checked, key=f"rota_{idx+1}")
            mostrar_rotas.append(mostrar)

        m = None
        cidades_marcadas = set()

        for idx, rota_info in enumerate(resultado.get("top_3", [])):
            if not mostrar_rotas[idx]:
                continue

            rota = rota_info["rota"]
            ruta_real = []
            for i in range(len(rota) - 1):
                coords_poly = obtener_polyline(rota[i], rota[i+1], coords_dict)
                if i > 0:
                    coords_poly = coords_poly[1:]
                ruta_real.extend(coords_poly)

            if m is None:
                lat_c, lng_c = ruta_real[0]
                m = folium.Map(location=[lat_c, lng_c], zoom_start=8)

            horas_rota = rota_info.get("tempo", 0) / 60.0

            folium.PolyLine(
                locations=ruta_real,
                color=cores[idx % len(cores)],
                weight=4,
                opacity=0.7,
                tooltip=(
                    f"Rota #{idx+1}: "
                    f"Custo: R$ {rota_info['custo']:.2f}, "
                    f"Distância: {rota_info.get('distancia', 0):.2f} km, "
                    f"Tempo: {horas_rota:.2f} h"
                )
            ).add_to(m)

            for (lat, lng), nome in zip([coords_dict[n] for n in rota], rota):
                if nome not in cidades_marcadas:
                    folium.CircleMarker(
                        location=[lat, lng],
                        radius=5,
                        color="black",
                        fill=True,
                        fill_color="yellow",
                        fill_opacity=0.7,
                        tooltip=nome
                    ).add_to(m)
                    cidades_marcadas.add(nome)

        if m:
            st_folium(m, width=800, height=500)
        else:
            st.info("Selecione pelo menos uma rota para visualizar o mapa.")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=resultado["historico"],
            x=list(range(1, len(resultado["historico"]) + 1)),
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Evolução do custo ao longo das iterações",
            xaxis_title="Iteração",
            yaxis_title="Custo (R$)",
            template="simple_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        for idx, rota_info in enumerate(resultado.get("top_3", [])):
            st.markdown(f"**Rota #{idx+1}:** {' → '.join(rota_info['rota'])}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f'<span style="font-size:1.1rem;font-weight:500;color:#000000">R$ {rota_info["custo"]:.2f}</span><br><span style="font-size:0.85rem;">Custo</span>',
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(
                    f'<span style="font-size:1.1rem;font-weight:500;color:#000000">{rota_info.get("distancia", 0):.2f} km</span><br><span style="font-size:0.85rem;">Distância</span>',
                    unsafe_allow_html=True
                )
            with c3:
                horas_rota = rota_info.get("tempo", 0) / 60.0
                st.markdown(
                    f'<span style="font-size:1.1rem;font-weight:500;color:#000000">{horas_rota:.2f} h</span><br><span style="font-size:0.85rem;">Tempo</span>',
                    unsafe_allow_html=True
                )

        tempo_exec = resultado.get("tempo_execucao", None)
        if tempo_exec is not None:
            st.info(f"Tempo de execução do algoritmo: {tempo_exec:.2f} segundos")
    else:
        st.info("Configure os parâmetros e clique em 'Executar ACO' para visualizar o resultado.")
