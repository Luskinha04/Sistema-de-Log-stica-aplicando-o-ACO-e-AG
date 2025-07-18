# import streamlit as st
# from streamlit_option_menu import option_menu
# import sys
# import os

# # Adiciona a pasta menu ao path para importação fácil
# sys.path.append(os.path.join(os.path.dirname(__file__), "menu"))

# # Importa cada página
# import parametros
# import aco
# import ga
# import comparacao
# import sobre

# st.set_page_config(page_title="Otimização de rotas", layout="wide", page_icon="🚚")

# menu_options = [
#     "Início",
#     "Parâmetros",
#     "ACO",
#     "Algoritmo genético",
#     "Comparação",
#     "Sobre"
# ]
# menu_icons = [
#     "house", "gear", "ant", "diagram-3", "bar-chart", "info-circle"
# ]
# # "bug" = inseto (alternativa para formiga), "diagram-3" para genética (substituto para DNA)
# MENU_KEY = "menu_selected_option"

# if MENU_KEY not in st.session_state:
#     st.session_state[MENU_KEY] = menu_options[0]
# active_page = st.session_state[MENU_KEY]

# with st.sidebar:
#     st.title("🚚 Otimização de rotas")
#     selected = option_menu(
#         menu_title=None,
#         options=menu_options,
#         icons=menu_icons,
#         menu_icon="cast",
#         default_index=menu_options.index(active_page),
#         key=MENU_KEY,
#         orientation="vertical"
#     )

# if selected == "Início":
#     st.header("Bem-vindo ao otimizador de rotas")
#     st.write("""
#         Este sistema compara algoritmos de Colônia de Formigas (ACO) e Algoritmo Genético (GA)
#         para roteamento eficiente de veículos. Use o menu ao lado para acessar as funcionalidades.
#     """)

# elif selected == "Parâmetros":
#     parametros.render()

# elif selected == "ACO":
#     aco.render()

# elif selected == "Algoritmo genético":
#     ga.render()

# elif selected == "Comparação":
#     comparacao.render()

# elif selected == "Sobre":
#     sobre.render()

# else:
#     st.error("Página não reconhecida.")








import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

# Adiciona a pasta menu ao path para importação fácil
sys.path.append(os.path.join(os.path.dirname(__file__), "menu"))

# Importa cada página
import parametros
import aco
import ga
import comparacao
import sobre

st.set_page_config(
    page_title="Otimização de rotas",
    layout="wide",
    page_icon="🚚"
)

menu_options = [
    "Início",
    "Parâmetros",
    "🐜 ACO",
    "🧬 GA",
    "Comparação",
    # "Sobre"
]
menu_icons = [
    # "house", "gear", "transparency", "transparency", "bar-chart", "info-circle"
    "house", "gear", "transparency", "transparency", "bar-chart"
]
MENU_KEY = "menu_selected_option"

if MENU_KEY not in st.session_state:
    st.session_state[MENU_KEY] = menu_options[0]
active_page = st.session_state[MENU_KEY]

with st.sidebar:
    st.title("🚚 Otimização de rotas")
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        menu_icon="cast",
        default_index=menu_options.index(active_page),
        key=MENU_KEY,
        orientation="vertical"
    )

if selected == "Início":
    st.markdown("""
    <div style="display:flex;align-items:center;">
        <span style="font-size:3rem; margin-right:1rem;">🚚</span>
        <h1 style="display:inline;">Sistema de Otimização de Rotas</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <br>
    <h3 style="color:#2c3e50;">Bem-vindo!</h3>
    <p style="font-size:1.1rem;">
        Este sistema foi desenvolvido com objetivo acadêmico para comparar técnicas de inteligência computacional aplicadas ao <b>problema de roteamento de veículos (VRP)</b>, utilizando:
        <ul>
            <li><b>Colônia de formigas (ACO))</b>: inspiração no comportamento coletivo das formigas para encontrar rotas eficientes.</li>
            <li><b>Algoritmo genético (GA))</b>: baseado nos princípios da evolução e seleção natural.</li>
        </ul>
        Explore as abas no menu lateral para definir os parâmetros, rodar cada algoritmo e comparar seus desempenhos em múltiplos cenários.<br><br>
        <b>Funcionalidades principais:</b>
        <ul>
            <li>Configuração flexível de parâmetros de simulação</li>
            <li>Visualização interativa das melhores rotas no mapa</li>
            <li>Gráficos comparativos de custo, distância e tempo</li>
            <li>Análise estatística de múltiplas execuções</li>
        </ul>
    </p>
    """, unsafe_allow_html=True)

    

# elif selected == "Parâmetros":
#     parametros.render()

# elif selected == "🐜 ACO":
#     st.header("ACO – Algoritmo de colônia de Formigas")
#     st.markdown("""
#     <span style="color:#3e4144;font-size:1rem;">
#     Este método se inspira no comportamento coletivo das formigas na natureza para buscar soluções eficientes de roteamento. As formigas artificiais constroem rotas com base em feromônios e heurísticas de custo, explorando e otimizando caminhos ao longo das iterações.
#     </span>
#     """, unsafe_allow_html=True)
#     aco.render()

# elif selected == "🧬 GA":
#     st.header("Algoritmo Genético (GA)")
#     st.markdown("""
#     <span style="color:#3e4144;font-size:1rem;">
#     O Algoritmo Genético utiliza operadores evolutivos como seleção, cruzamento e mutação para evoluir populações de rotas ao longo das gerações, simulando o processo de seleção natural para encontrar soluções de alta qualidade para o VRP.
#     </span>
#     """, unsafe_allow_html=True)
#     ga.render()

# elif selected == "Comparação":
#     comparacao.render()

# elif selected == "Sobre":
#     sobre.render()

# else:
#     st.error("Página não reconhecida.")





elif selected == "Parâmetros":
    parametros.render()

elif selected == "🐜 ACO":
    aco.render()

elif selected == "🧬 GA":
    ga.render()

elif selected == "Comparação":
    comparacao.render()

else:
    st.error("Página não reconhecida.")
