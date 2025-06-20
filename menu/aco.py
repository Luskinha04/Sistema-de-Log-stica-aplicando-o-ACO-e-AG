# import streamlit as st
# import pandas as pd
# from algoritmos.aco import run_aco
# import folium
# from streamlit_folium import st_folium
# import json
# import os
# import plotly.graph_objects as go
# import time

# def render():
#     st.header("Algoritmo de colônia de formigas (ACO)")

#     matriz_custos = pd.read_csv("dados/matriz_custos.csv", index_col=0)
#     cidades = matriz_custos.index.tolist()

#     idx_patrocinio = cidades.index("Patrocínio") if "Patrocínio" in cidades else 0
#     cidade_inicio = st.selectbox("Cidade inicial/final", cidades, index=idx_patrocinio)

#     st.subheader("Parâmetros do ACO")
#     n_formigas = st.number_input("Número de formigas", 1, 100, 20)
#     n_iter = st.number_input("Número de iterações", 10, 10000, st.session_state.get("max_iter", 1000), step=10)
#     alfa = st.slider("Alfa (peso do feromônio)", 0.1, 5.0, 1.0, 0.1)
#     beta = st.slider("Beta (peso da heurística)", 0.1, 10.0, 5.0, 0.1)
#     evaporacao = st.slider("Taxa de evaporação", 0.01, 1.0, 0.5, 0.01)

#     if st.button("Executar ACO"):
#         idx_inicio = cidades.index(cidade_inicio)
#         t0 = time.time()
#         resultado = run_aco(
#             matriz_custos,
#             n_formigas=n_formigas,
#             n_iter=n_iter,
#             alfa=alfa,
#             beta=beta,
#             evaporacao=evaporacao,
#             cidade_inicio=idx_inicio
#         )
#         t1 = time.time()
#         resultado["tempo_execucao"] = t1 - t0
#         st.session_state["aco_resultado"] = resultado

#     if "aco_resultado" in st.session_state:
#         resultado = st.session_state["aco_resultado"]
#         st.success(f"Melhor rota encontrada: {' → '.join(resultado['rota'])}")
#         st.write(f"Custo total: R$ {resultado['custo']:.2f}")

#         # Visualização das três melhores rotas no mapa com checkboxes
#         with open("dados/municipios.json", encoding="utf-8") as f:
#             dados_cidades = json.load(f)
#         coords_dict = {d["nome"]: (d["lat"], d["lng"]) for d in dados_cidades}

#         # Emojis e cores para cada rota
#         cores = ["blue", "red", "orange"]
#         cores_emojis = ["🔵", "🔴", "🟠"]

#         # Checkboxes para mostrar/ocultar rotas        
#         colunas = st.columns(3)
#         mostrar_rotas = []
#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             checked = True if idx == 0 else False  # Exibe só a melhor rota por padrão
#             label = f"{cores_emojis[idx]} Rota #{idx+1} (Custo: R$ {rota_info['custo']:.2f})"
#             # Adiciona o checkbox na coluna correspondente
#             with colunas[idx]:
#                 mostrar = st.checkbox(label, value=checked, key=f"rota_{idx+1}")
#             mostrar_rotas.append(mostrar)

#         m = None
#         cidades_marcadas = set()

#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             if not mostrar_rotas[idx]:
#                 continue  # Não desenha esta rota se não estiver marcada

#             coordenadas = [coords_dict[nome] for nome in rota_info["rota"]]
#             if m is None:
#                 # Centraliza o mapa na primeira rota exibida
#                 lat_c, lng_c = coordenadas[0]
#                 m = folium.Map(location=[lat_c, lng_c], zoom_start=8)

#             # Adiciona linha colorida para a rota selecionada
#             folium.PolyLine(
#                 locations=coordenadas,
#                 color=cores[idx % len(cores)],
#                 weight=4,
#                 opacity=0.7,
#                 tooltip=f"Rota #{idx+1}: Custo R$ {rota_info['custo']:.2f}"
#             ).add_to(m)

#             # Marca as cidades apenas uma vez
#             for (lat, lng), nome in zip(coordenadas, rota_info["rota"]):
#                 if nome not in cidades_marcadas:
#                     folium.CircleMarker(
#                         location=[lat, lng],
#                         radius=5,
#                         color="black",
#                         fill=True,
#                         fill_color="yellow",
#                         fill_opacity=0.7,
#                         tooltip=nome
#                     ).add_to(m)
#                     cidades_marcadas.add(nome)

#         if m:
#             st_folium(m, width=800, height=500)
#         else:
#             st.info("Selecione pelo menos uma rota para visualizar o mapa.")

#         # Gráfico de evolução do custo
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             y=resultado["historico"],
#             x=list(range(1, len(resultado["historico"]) + 1)),
#             mode='lines+markers'
#         ))
#         fig.update_layout(
#             title="Evolução do custo ao longo das iterações",
#             xaxis_title="Iteração",
#             yaxis_title="Custo (R$)",
#             template="simple_white"
#         )
#         st.plotly_chart(fig, use_container_width=True)

#         # Exibição das métricas comparativas
#         tempo_exec = resultado.get("tempo_execucao", None)
#         if tempo_exec is not None:
#             st.info(f"Tempo de execução do algoritmo: {tempo_exec:.2f} segundos")
#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             st.markdown(f"**Rota #{idx+1}:** {' → '.join(rota_info['rota'])}")
#             st.write(f"Custo total: R$ {rota_info['custo']:.2f}")
#     else:
#         st.info("Configure os parâmetros e clique em 'Executar ACO' para visualizar o resultado.")









# import streamlit as st
# import pandas as pd
# from algoritmos.aco import run_aco
# import folium
# from streamlit_folium import st_folium
# import json
# import os
# import plotly.graph_objects as go
# import time

# def render():
#     st.header("Algoritmo de colônia de formigas (ACO)")

#     matriz_custos = pd.read_csv("dados/matriz_custos.csv", index_col=0)
#     matriz_distancias = pd.read_csv("dados/matriz_distancias.csv", index_col=0)
#     matriz_tempos = pd.read_csv("dados/matriz_tempos.csv", index_col=0)
#     cidades = matriz_custos.index.tolist()

#     idx_patrocinio = cidades.index("Patrocínio") if "Patrocínio" in cidades else 0
#     cidade_inicio = st.selectbox("Cidade inicial/final", cidades, index=idx_patrocinio)

#     st.subheader("Parâmetros do ACO")
#     n_formigas = st.number_input("Número de formigas", 1, 100, 20)
#     n_iter = st.number_input("Número de iterações", 10, 10000, st.session_state.get("max_iter", 1000), step=10)
#     alfa = st.slider("Alfa (peso do feromônio)", 0.1, 5.0, 1.0, 0.1)
#     beta = st.slider("Beta (peso da heurística)", 0.1, 10.0, 5.0, 0.1)
#     evaporacao = st.slider("Taxa de evaporação", 0.01, 1.0, 0.5, 0.01)

#     if st.button("Executar ACO"):
#         idx_inicio = cidades.index(cidade_inicio)
#         t0 = time.time()
#         resultado = run_aco(
#             matriz_custos,
#             matriz_distancias,
#             matriz_tempos,
#             n_formigas=n_formigas,
#             n_iter=n_iter,
#             alfa=alfa,
#             beta=beta,
#             evaporacao=evaporacao,
#             cidade_inicio=idx_inicio
#         )
#         t1 = time.time()
#         resultado["tempo_execucao"] = t1 - t0
#         st.session_state["aco_resultado"] = resultado

#     if "aco_resultado" in st.session_state:
#         resultado = st.session_state["aco_resultado"]
#         st.success(f"Melhor rota encontrada: {' → '.join(resultado['rota'])}")

#         # Mostra custo, distância e tempo da melhor rota em 3 colunas
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Custo total (R$)", f"{resultado['custo']:.2f}")
#         col2.metric("Distância total (km)", f"{resultado['distancia']:.2f}")
#         col3.metric("Tempo total (min)", f"{resultado['tempo']:.2f}")

#         # Visualização das três melhores rotas no mapa com checkboxes
#         with open("dados/municipios.json", encoding="utf-8") as f:
#             dados_cidades = json.load(f)
#         coords_dict = {d["nome"]: (d["lat"], d["lng"]) for d in dados_cidades}

#         cores = ["blue", "red", "orange"]
#         cores_emojis = ["🔵", "🔴", "🟠"]

#         colunas = st.columns(3)
#         mostrar_rotas = []
#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             checked = True if idx == 0 else False
#             label = f"{cores_emojis[idx]} Rota #{idx+1} (Custo: R$ {rota_info['custo']:.2f})"
#             with colunas[idx]:
#                 mostrar = st.checkbox(label, value=checked, key=f"rota_{idx+1}")
#             mostrar_rotas.append(mostrar)

#         m = None
#         cidades_marcadas = set()

#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             if not mostrar_rotas[idx]:
#                 continue

#             coordenadas = [coords_dict[nome] for nome in rota_info["rota"]]
#             if m is None:
#                 lat_c, lng_c = coordenadas[0]
#                 m = folium.Map(location=[lat_c, lng_c], zoom_start=8)

#             folium.PolyLine(
#                 locations=coordenadas,
#                 color=cores[idx % len(cores)],
#                 weight=4,
#                 opacity=0.7,
#                 tooltip=(
#                     f"Rota #{idx+1}: "
#                     f"Custo: R$ {rota_info['custo']:.2f}, "
#                     f"Distância: {rota_info.get('distancia', 0):.2f} km, "
#                     f"Tempo: {rota_info.get('tempo', 0):.2f} min"
#                 )
#             ).add_to(m)

#             # Marca as cidades apenas uma vez
#             for (lat, lng), nome in zip(coordenadas, rota_info["rota"]):
#                 if nome not in cidades_marcadas:
#                     folium.CircleMarker(
#                         location=[lat, lng],
#                         radius=5,
#                         color="black",
#                         fill=True,
#                         fill_color="yellow",
#                         fill_opacity=0.7,
#                         tooltip=nome
#                     ).add_to(m)
#                     cidades_marcadas.add(nome)

#         if m:
#             st_folium(m, width=800, height=500)
#         else:
#             st.info("Selecione pelo menos uma rota para visualizar o mapa.")

#         # Gráfico de evolução do custo
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             y=resultado["historico"],
#             x=list(range(1, len(resultado["historico"]) + 1)),
#             mode='lines+markers'
#         ))
#         fig.update_layout(
#             title="Evolução do custo ao longo das iterações",
#             xaxis_title="Iteração",
#             yaxis_title="Custo (R$)",
#             template="simple_white"
#         )
#         st.plotly_chart(fig, use_container_width=True)

#         # Exibição das métricas comparativas para as 3 melhores rotas em 3 colunas
#         for idx, rota_info in enumerate(resultado.get("top_3", [])):
#             st.markdown(f"**Rota #{idx+1}:** {' → '.join(rota_info['rota'])}")
#             c1, c2, c3 = st.columns(3)
#             c1.metric("Custo (R$)", f"{rota_info['custo']:.2f}")
#             c2.metric("Distância (km)", f"{rota_info.get('distancia', 0):.2f}")
#             c3.metric("Tempo (min)", f"{rota_info.get('tempo', 0):.2f}")

#         tempo_exec = resultado.get("tempo_execucao", None)
#         if tempo_exec is not None:
#             st.info(f"Tempo de execução do algoritmo: {tempo_exec:.2f} segundos")
#     else:
#         st.info("Configure os parâmetros e clique em 'Executar ACO' para visualizar o resultado.")








import streamlit as st
import pandas as pd
from algoritmos.aco import run_aco
import folium
from streamlit_folium import st_folium
import json
import os
import plotly.graph_objects as go
import time

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



        # Salva os parâmetros usados para a comparação múltipla
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
            # (não inclua 'seed', pois será definida na execução múltipla)
        ]



        resultado["tempo_execucao"] = t1 - t0
        st.session_state["aco_resultado"] = resultado
        # Guarda para comparativo (pronto para ler em outra seção)
        st.session_state["aco_resultados_comparativo"] = {
            "rota": resultado["rota"],
            "custo": resultado["custo"],
            "distancia": resultado["distancia"],
            "tempo": resultado["tempo"],  # Em minutos, mas já mostramos convertido abaixo
            "historico": resultado["historico"],
            "top_3": resultado["top_3"],
            "tempo_execucao": resultado["tempo_execucao"]
        }

    if "aco_resultado" in st.session_state:
        resultado = st.session_state["aco_resultado"]
        st.success(f"Melhor rota encontrada: {' → '.join(resultado['rota'])}")

        # Mostra custo, distância e tempo da melhor rota em 3 colunas (com CSS customizado)
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

        # Visualização das três melhores rotas no mapa com checkboxes
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

            coordenadas = [coords_dict[nome] for nome in rota_info["rota"]]
            if m is None:
                lat_c, lng_c = coordenadas[0]
                m = folium.Map(location=[lat_c, lng_c], zoom_start=8)

            horas_rota = rota_info.get("tempo", 0) / 60.0

            folium.PolyLine(
                locations=coordenadas,
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

            for (lat, lng), nome in zip(coordenadas, rota_info["rota"]):
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

        # Gráfico de evolução do custo
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

        # Exibição das métricas comparativas para as 3 melhores rotas em 3 colunas
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
