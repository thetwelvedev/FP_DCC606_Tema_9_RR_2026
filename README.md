# FP_DCC606_Tema_9_RR_2026

## Verificação Formal de Algoritmos de Roteamento para Sistemas Ciberfísicos de Logística Autônoma

## Projeto Prático de Verificação de Sistemas / Métodos Formais

---

**Integrantes:** [Leonardo Castro](https://github.com/thetwelvedev) e [Álefe Alves](https://github.com/AlefeAlvesC)

**Descrição:** Este projeto consiste no design, fundamentação teórica e implementação de um protótipo de **Executor Simbólico** em ambiente Python integrado ao motor de inferência lógica e solver SMT **Z3 Prover**. O sistema é capaz de injetar variáveis simbólicas em um algoritmo de otimização de rotas (baseado no Problema do Caixeiro Viajante - TSP) para provar formalmente a segurança e a corretude de suas saídas frente a restrições dinâmicas de contorno em Sistemas Ciberfísicos (CPS).

---

## Índice

* [Verificação Formal de Algoritmos de Roteamento para Sistemas Ciberfísicos de Logística Autônoma](https://www.google.com/search?q=%23verifica%C3%A7%C3%A3o-formal-de-algoritmos-de-roteamento-para-sistemas-ciberf%C3%ADsicos-de-log%C3%ADstica-aut%C3%B4noma)
* [Projeto Prático de Verificação de Sistemas / Métodos Formais](https://www.google.com/search?q=%23projeto-pr%C3%A1tico-de-verifica%C3%A7%C3%A3o-de-sistemas--m%C3%A9todos-formais)
* [Índice](https://www.google.com/search?q=%23%C3%ADndice)
* [Descrição do Projeto](https://www.google.com/search?q=%23descri%C3%A7%C3%A3o-do-projeto)
* [Funcionalidades](https://www.google.com/search?q=%23funcionalidades)
* [Estrutura do Projeto](https://www.google.com/search?q=%23estrutura-do-projeto)
* [Bibliotecas e Ferramentas Utilizadas](https://www.google.com/search?q=%23bibliotecas-e-ferramentas-utilizadas)
* [Formulação Matemática](https://www.google.com/search?q=%23formula%C3%A7%C3%A3o-matem%C3%A1tica)
* [Relatório Técnico e Resenha Crítica](https://www.google.com/search?q=%23relat%C3%B3rio-t%C3%A9cnico-e-resenha-cr%C3%ADtica)
* [Referências](https://www.google.com/search?q=%23refer%C3%AAncias)



---

## Descrição do Projeto

Em ambientes de missão crítica (como drones de suprimento médico ou robôs industriais), testes de caixa-preta tradicionais são insuficientes para cobrir o espaço de estados discretos de algoritmos combinatórios.

Este ecossistema utiliza **Execução Simbólica** para substituir entradas numéricas concretas (distâncias e custos) por símbolos matemáticos. Ao longo do fluxo de controle, o programa gera equações lógicas chamadas *Path Conditions* (Condições de Caminho). Se um estado de erro ou violação de restrição for logicamente satisfatível (`SAT`), o motor Z3 descobre o contraexemplo exato que causaria a falha do sistema. Caso contrário (`UNSAT`), o algoritmo é matematicamente provado seguro.

---

## Funcionalidades

* **Instanciação Simbólica:** Substituição de matrizes de adjacência estáticas por objetos simbólicos lineares e reais.
* **Motor de Asserção (Injeção de Invariantes):** Validação matemática que impede a formação de sub-rotas disjuntas através da formulação MTZ.


* **Análise de Inviabilidade:** Diferenciação rigorosa entre cenários de caminhos válidos e provas matemáticas de segurança absoluta.
* **Ensaios de Estresse e Escalabilidade:** Protocolo experimental automatizado para medir o tempo de inferência e geração de conflitos conforme o grafo escala.



---

## Estrutura do Projeto

Abaixo está a estrutura de diretórios consolidada do ecossistema do verificador formal:

```text
.
├── docs/
│   ├── img/
│   │   ├── grafico_clausulas.png
│   │   ├── grafico_conflitos.png
│   │   └── grafico_tempo.png
│   └── artigo_AA_projeto_final.pdf
├── resultados/
│   ├── grafico_clausulas.png
│   ├── grafico_conflitos.png
│   ├── grafico_tempo.png
│   └── resultados.csv
├── src/
│   ├── __pycache__/
│   ├── executor simbólico.py
│   ├── main.py
│   └── modelagem_mtz.py
├── .gitignore
├── gerar gráficos.py
├── LICENSE
├── README.md
└── requirements.txt

```

### Descrição dos Arquivos Principais

* **`docs/artigo_AA_projeto_final.pdf`**: Documento acadêmico completo detalhando a verificação formal de algoritmos de roteamento para Sistemas Ciberfísicos (CPS) autônomos.


* **`src/main.py`**: Ponto de entrada do sistema que define a *seed* de reprodutibilidade e orquestra a injeção de falhas.


* **`src/executor simbólico.py`**: Módulo responsável por automatizar os ensaios de estresse computacional para os diferentes tamanhos de matrizes.


* **`src/modelagem_mtz.py`**: Contém o coração matemático do projeto, estabelecendo o Z3 Solver, declarando os tensores simbólicos (x, d, u) e as funções de cálculo de quebra de energia.


* **`gerar gráficos.py`**: Script utilitário para a geração visual das métricas de desempenho.
* **`resultados/`**: Diretório que armazena as saídas empíricas do *solver*, incluindo o crescimento exponencial de cláusulas, tempo e conflitos à medida que a dimensão do grafo aumenta.



---

## Bibliotecas e Ferramentas Utilizadas

### z3-solver

> Usado para:

* Instanciar variáveis simbólicas inteiras (`z3.Int()`) e reais (`z3.Real()`).
* Processar as cláusulas geradas pelas restrições físicas do grafo através da arquitetura DPLL(T).


* Resolver as condições de caminho e gerar contraexemplos através do motor CDCL interno do solver da Microsoft Research.



### pytest

> Usado para:

* Automatizar os testes unitários do motor de asserção.
* Validar as matrizes base de controle de dimensões pequenas (4x4 e 5x5).



### time & os

> Usado para:

* Monitorar o tempo exato de inferência do solver em milissegundos (ms).


* Gerenciar a persistência das métricas e relatórios de estresse computacional.

---

## Formulação Matemática

O problema de decisão inserido no contexto SMT para a eliminação de sub-rotas baseia-se na formulação de **Miller-Tucker-Zemlin (MTZ)**:

$$\min \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} d_{ij} \cdot x_{ij}$$

**Sujeito a:**

* $\sum_{j=0, j \neq i}^{n-1} x_{ij} = 1, \quad \forall i \in V$ (Conservação de fluxo de saída)
* $\sum_{i=0, i \neq j}^{n-1} x_{ij} = 1, \quad \forall j \in V$ (Conservação de fluxo de entrada)
* $u_i - u_j + n \cdot x_{ij} \le n - 1, \quad \forall i, j \in \{1, \dots, n-1\}, \, i \neq j$ (Eliminação de sub-rotas)
* $\sum_{i=0}^{n-1} \sum_{j=0}^{n-1} d_{ij} \cdot x_{ij} > C_{\max}$ (Condição de busca por falhas/vulnerabilidades)

---

## Relatório Técnico e Resenha Crítica

O projeto é fundamentado em duas grandes frentes teóricas detalhadas em nosso relatório:

1. **Análise do Artigo Seminal de James C. King (1976):** *Symbolic Execution and Program Testing*, discutindo a evolução do conceito de memória simbólica e árvores de execução para as ferramentas modernas.


2. **Estudo de Complexidade dos Algoritmos do Z3:** Análise assintótica de pior caso do algoritmo CDCL para SAT, da arquitetura DPLL(T) para teorias combinadas e das heurísticas de *E-matching* para quantificadores.



[Acesse o Artigo](/docs/artigo_AA_projeto_final.pdf)

---

## Referências

* KING, James C. Symbolic execution and program testing. *Communications of the ACM*, vol. 19, n. 7, p. 385–394, 1976. DOI: 10.1145/360248.360252.
* DE MOURA, Leonardo; BJØRNER, Nikolaj. Z3: An efficient SMT solver. In: *International Conference on Tools and Algorithms for the Construction and Analysis of Systems*. Springer, Berlin, Heidelberg, 2008. p. 337-340.
* MILLER, Clair E.; TUCKER, Albert W.; ZEMLIN, Lowell A. Integer programming formulation of traveling salesman problems. *Journal of the ACM (JACM)*, vol. 7, n. 4, p. 326-329, 1960.