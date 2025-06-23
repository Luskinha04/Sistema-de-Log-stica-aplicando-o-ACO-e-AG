# 🚚 Otimização de Rotas com ACO e Algoritmo Genético

Este projeto foi desenvolvido como parte da disciplina de **Inteligência Computacional** no curso de Análise e Desenvolvimento de Sistemas do IFTM. O objetivo é aplicar algoritmos de **Colônia de Formigas (ACO)** e **Algoritmo Genético (GA)** na otimização de rotas logísticas de transporte de café entre municípios do **Alto Paranaíba (MG)**.

---

## 📁 Estrutura do Projeto

```
📦 main/
├── algoritmos/
│   ├── aco.py                 # Implementação do algoritmo ACO
│   ├── ga.py                  # Implementação do Algoritmo Genético
│   ├── distancia_tempo.py     # Geração das matrizes de distância e tempo
│   ├── matriz_custos.py       # Manipulação da matriz de custos
│   └── parametros.py          # Parâmetros gerais dos algoritmos
│
├── dados/
│   ├── matriz_custos.csv      # Matriz de custos entre os municípios
│   ├── matriz_distancias.csv  # Matriz de distâncias
│   ├── matriz_tempos.csv      # Matriz de tempos de deslocamento
│   ├── municipios.json        # Lista de municípios com coordenadas
│   └── municipios_teste1.json # Versão reduzida de municípios para teste
│
├── menu/
│   ├── aco.py                 # Interface interativa do ACO
│   ├── ga.py                  # Interface interativa do GA
│   ├── comparacao.py          # Comparação entre ACO e GA
│   ├── parametros.py          # Ajuste de parâmetros via interface
│   └── sobre.py               # Informações do projeto
│
├── main.py                    # Arquivo principal que executa o menu Streamlit
├── requirements.txt           # Lista de dependências do projeto
```

---

## 🎯 Objetivo do Projeto

Desenvolver um sistema capaz de propor e comparar rotas otimizadas para o transporte de café entre os municípios da região, utilizando:

* 🐜 **Algoritmo de Colônia de Formigas (ACO)**
* 🧬 **Algoritmo Genético (GA)**

---

## 💻 Tecnologias e Bibliotecas

* **Python 3.10+**
* **Streamlit** – para a interface interativa
* **Pandas** – manipulação de dados
* **NetworkX** – construção e visualização dos grafos de rotas
* **Google Maps API** – integração para rotas reais

---

## 📌 Funcionalidades

* Definição e visualização de rotas otimizadas com ACO e GA
* Comparação entre as rotas encontradas por cada algoritmo
* Visualização de métricas: distância, tempo, custo
* Integração com mapa real (API Google Maps)
* Interface simples e intuitiva via **Streamlit**

---

## 🚀 Como Executar

1. Clone o repositório:

```
git clone https://github.com/Luskinha04/Sistema-de-Log-stica
cd Sistema-de-Log-stica
```

2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Execute a aplicação:

```
streamlit run main.py
```

---

## 🔑 Sobre a API Key do Google

Para visualizar rotas reais, é necessário possuir uma API Key do Google com as seguintes permissões:

* **Maps JavaScript API**
* **Distance Matrix API**
* **Directions API**

---

## 📊 Dados Utilizados

As rotas foram baseadas em um conjunto de municípios da região do **Alto Paranaíba**, com distâncias simuladas ou obtidas via API. Os dados estão disponíveis em `dados/`.

---

## 📈 Resultados Esperados

O sistema exibe:

* A melhor rota de cada algoritmo
* As três melhores rotas com cores distintas
* Comparações de métricas (tempo de execução, custo, etc.)
* Interface visual com o mapa e métricas organizadas

---

## 👨‍🏫 Sobre o Projeto

Trabalho individual para avaliação na disciplina de **Inteligência Computacional**, com foco em **Metaheurísticas** aplicadas a um **problema de roteamento logístico**.

---

> **IFTM - Instituto Federal do Triângulo Mineiro  
> **Curso:** Análise e Desenvolvimento de Sistemas  
> **Disciplina:** Inteligência Computacional
> **Período:** 6º Semestre

---
