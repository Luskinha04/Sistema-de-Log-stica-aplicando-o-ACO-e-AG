# # menu/parametros.py
# import streamlit as st
# from algoritmos.matriz_custos import calcular_matriz_custos
# import pandas as pd
# import os

# def render():
#     st.header("Configuração de parâmetros globais")
#     st.write("Defina aqui os custos e parâmetros dos algoritmos. As alterações só terão efeito ao clicar em 'Atualizar parâmetros e matriz de custos'.")

#     # Parâmetros globais de custo (inputs temporários)
#     custo_km = st.number_input("Custo por quilômetro (R$)", min_value=0.0, max_value=100.0, value=st.session_state.get("custo_km", 2.5), step=0.1)
#     custo_min = st.number_input("Custo por minuto (R$)", min_value=0.0, max_value=100.0, value=st.session_state.get("custo_min", 0.5), step=0.1)

#     # Parâmetros dos algoritmos
#     max_iter = st.number_input("Máximo de iterações", min_value=10, max_value=5000, value=st.session_state.get("max_iter", 1000), step=10)
#     tempo_limite = st.number_input("Tempo máximo de execução (segundos)", min_value=10, max_value=3600, value=st.session_state.get("tempo_limite", 300), step=10)

#     if st.button("Atualizar parâmetros e matriz de custos"):
#         # Atualiza sessão
#         st.session_state["custo_km"] = custo_km
#         st.session_state["custo_min"] = custo_min
#         st.session_state["max_iter"] = int(max_iter)
#         st.session_state["tempo_limite"] = int(tempo_limite)

#         # Calcula e salva matriz de custos
#         custos = calcular_matriz_custos(
#             custo_km=custo_km,
#             custo_min=custo_min
#         )
#         st.success("Parâmetros atualizados e matriz de custos recalculada com sucesso!")
#         st.dataframe(custos)
#         st.download_button(
#             "Baixar matriz de custos (CSV)",
#             data=custos.to_csv().encode("utf-8"),
#             file_name="matriz_custos.csv",
#             mime="text/csv"
#         )
#     else:
#         # Mostra última matriz de custos, se existir
#         path_custos = "dados/matriz_custos.csv"
#         if os.path.exists(path_custos):
#             custos = pd.read_csv(path_custos, index_col=0)
#             st.info("Última matriz de custos calculada:")
#             st.dataframe(custos)
#             st.download_button(
#                 "Baixar matriz de custos (CSV)",
#                 data=custos.to_csv().encode("utf-8"),
#                 file_name="matriz_custos.csv",
#                 mime="text/csv"
#             )
#         else:
#             st.info("Nenhuma matriz de custos foi gerada ainda.")











# menu/parametros.py
import streamlit as st
from algoritmos.matriz_custos import calcular_matriz_custos
import pandas as pd
import os

def render():
    st.header("Configuração de parâmetros globais")
    st.write("Defina aqui os custos e parâmetros dos algoritmos. As alterações só terão efeito ao clicar em 'Atualizar parâmetros e matriz de custos'.")

    # Parâmetros globais de custo (inputs temporários)
    custo_km = st.number_input(
        "Custo por quilômetro (R$)", min_value=0.0, max_value=100.0,
        value=st.session_state.get("custo_km", 2.5), step=0.1
    )
    custo_min = st.number_input(
        "Custo por minuto (R$)", min_value=0.0, max_value=100.0,
        value=st.session_state.get("custo_min", 0.5), step=0.1
    )

    # Parâmetros dos algoritmos
    max_iter = st.number_input(
        "Máximo de iterações", min_value=10, max_value=5000,
        value=st.session_state.get("max_iter", 1000), step=10
    )
    tempo_limite = st.number_input(
        "Tempo máximo de execução (segundos)", min_value=10, max_value=3600,
        value=st.session_state.get("tempo_limite", 300), step=10
    )

    if st.button("Atualizar parâmetros e matriz de custos"):
        # Atualiza sessão
        st.session_state["custo_km"] = custo_km
        st.session_state["custo_min"] = custo_min
        st.session_state["max_iter"] = int(max_iter)
        st.session_state["tempo_limite"] = int(tempo_limite)

        # Calcula e salva matriz de custos
        custos = calcular_matriz_custos(
            custo_km=custo_km,
            custo_min=custo_min
        )
        st.success("Parâmetros atualizados e matriz de custos recalculada com sucesso!")
        st.dataframe(custos)
        st.download_button(
            "Baixar matriz de custos (CSV)",
            data=custos.to_csv().encode("utf-8"),
            file_name="matriz_custos.csv",
            mime="text/csv"
        )
    else:
        # Mostra última matriz de custos, se existir
        path_custos = "dados/matriz_custos.csv"
        if os.path.exists(path_custos):
            custos = pd.read_csv(path_custos, index_col=0)
            st.info("Última matriz de custos calculada:")
            st.dataframe(custos)
            st.download_button(
                "Baixar matriz de custos (CSV)",
                data=custos.to_csv().encode("utf-8"),
                file_name="matriz_custos.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhuma matriz de custos foi gerada ainda.")

    # --- NOVA FUNCIONALIDADE: Editar trecho específico ao final ---
    st.divider()
    st.subheader("Editar trecho específico entre dois municípios")

    # Caminhos dos arquivos das matrizes
    path_dist = "dados/matriz_distancias.csv"
    path_temp = "dados/matriz_tempos.csv"
    path_custos = "dados/matriz_custos.csv"
    cidades = None

    # # Tenta carregar uma das matrizes para pegar os municípios
    # if os.path.exists(path_dist):
    #     matriz_dist = pd.read_csv(path_dist, index_col=0)
    #     cidades = matriz_dist.index.tolist()
    # elif os.path.exists(path_temp):
    #     matriz_temp = pd.read_csv(path_temp, index_col=0)
    #     cidades = matriz_temp.index.tolist()
    # elif os.path.exists(path_custos):
    #     matriz_custos = pd.read_csv(path_custos, index_col=0)
    #     cidades = matriz_custos.index.tolist()

    # Tenta carregar as matrizes, se existirem
    if os.path.exists(path_dist):
        matriz_dist = pd.read_csv(path_dist, index_col=0)
        cidades = matriz_dist.index.tolist()
    if os.path.exists(path_temp):
        matriz_temp = pd.read_csv(path_temp, index_col=0)
        if cidades is None:
            cidades = matriz_temp.index.tolist()
    if os.path.exists(path_custos):
        matriz_custos = pd.read_csv(path_custos, index_col=0)
        if cidades is None:
            cidades = matriz_custos.index.tolist()




    if cidades is not None:
        col1, col2 = st.columns(2)
        with col1:
            municipio_a = st.selectbox("Origem", cidades, key="trecho_a")
        with col2:
            municipio_b = st.selectbox("Destino", cidades, key="trecho_b")

        if municipio_a != municipio_b:
            # Valores atuais, se disponíveis
            dist_atual = matriz_dist.loc[municipio_a, municipio_b] if os.path.exists(path_dist) else 0.0
            temp_atual = matriz_temp.loc[municipio_a, municipio_b] if os.path.exists(path_temp) else 0.0
            custo_atual = matriz_custos.loc[municipio_a, municipio_b] if os.path.exists(path_custos) else 0.0

            st.markdown(
                f"**Valores atuais:** Distância: `{dist_atual:.2f} km` | Tempo: `{temp_atual:.2f} min` | Custo: `R$ {custo_atual:.2f}`"
            )

            nova_dist = st.number_input(
                "Nova distância (km)", min_value=0.0, value=float(dist_atual), step=0.1, key="nova_dist"
            )
            novo_temp = st.number_input(
                "Novo tempo (minutos)", min_value=0.0, value=float(temp_atual), step=1.0, key="novo_temp"
            )

            if st.button("Atualizar trecho selecionado"):
                # Atualiza arquivos, caso existam
                atualizado = False

                if os.path.exists(path_dist):
                    matriz_dist.loc[municipio_a, municipio_b] = nova_dist
                    matriz_dist.to_csv(path_dist)
                    atualizado = True
                if os.path.exists(path_temp):
                    matriz_temp.loc[municipio_a, municipio_b] = novo_temp
                    matriz_temp.to_csv(path_temp)
                    atualizado = True
                novo_custo = custo_km * nova_dist + custo_min * novo_temp
                if os.path.exists(path_custos):
                    matriz_custos.loc[municipio_a, municipio_b] = novo_custo
                    matriz_custos.to_csv(path_custos)
                    atualizado = True

                if atualizado:
                    st.success(
                        f"Trecho {municipio_a} ➔ {municipio_b} atualizado para: "
                        f"{nova_dist:.2f} km, {novo_temp:.2f} min, R$ {novo_custo:.2f}."
                    )
                else:
                    st.warning("Não foi possível atualizar os arquivos. Verifique se as matrizes existem.")
        else:
            st.info("Escolha municípios diferentes para editar o trecho.")

    else:
        st.info("Nenhuma matriz foi encontrada em dados/. Execute ao menos uma simulação primeiro.")



