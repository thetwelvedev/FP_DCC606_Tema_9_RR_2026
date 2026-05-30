# FP_DCC606_Tema_9_RR_2026
## Verificação Formal de Algoritmos de Roteamento para Sistemas Ciberfísicos de Logística Autônoma

## Projeto Prático de Verificação de Sistemas / Métodos Formais

---

**Integrantes:** [Leonardo Castro](https://github.com/thetwelvedev) e [Álefe Alves](https://github.com/AlefeAlvesC)

**Descrição:** Este projeto consiste no design, fundamentação teórica e implementação de um protótipo de **Executor Simbólico** em ambiente Python integrado ao motor de inferência lógica e solver SMT **Z3 Prover**. O sistema é capaz de injetar variáveis simbólicas em um algoritmo de otimização de rotas (baseado no Problema do Caixeiro Viajante - TSP) para provar formalmente a segurança e a corretude de suas saídas frente a restrições dinâmicas de contorno em Sistemas Ciberfísicos (CPS).

---

## Índice
- [Verificação Formal de Algoritmos de Roteamento para Sistemas Ciberfísicos de Logística Autônoma](#verificação-formal-de-algoritmos-de-roteamento-para-sistemas-ciberfísicos-de-logística-autônoma)
  - [Projeto Prático de Verificação de Sistemas / Métodos Formais](#projeto-prático-de-verificação-de-sistemas--métodos-formais)
  - [Índice](#índice)
  - [Descrição do Projeto](#descrição-do-projeto)
  - [Funcionalidades](#funcionalidades)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Bibliotecas e Ferramentas Utilizadas](#bibliotecas-e-ferramentas-utilizadas)
    - [z3-solver](#z3-solver)
    - [pytest](#pytest)
    - [time \& os](#time--os)
  - [Formulação Matemática](#formulação-matemática)
  - [Relatório Técnico e Resenha Crítica](#relatório-técnico-e-resenha-crítica)
  - [Referências](#referências)

---

## Descrição do Projeto

Em ambientes de missão crítica (como drones de suprimento médico ou robôs industriais), testes de caixa-preta tradicionais são insuficientes para cobrir o espaço de estados discretos de algoritmos combinatórios. 

Este ecossistema utiliza **Execução Simbólica** para substituir entradas numéricas concretas (distâncias e custos) por símbolos matemáticos. Ao longo do fluxo de controle, o programa gera equações lógicas chamadas *Path Conditions* (Condições de Caminho). Se um estado de erro ou violação de restrição for logicamente satisfatível (`SAT`), o motor Z3 descobre o contraexemplo exato que causaria a falha do sistema. Caso contrário (`UNSAT`), o algoritmo é matematicamente provado seguro.

---

## Funcionalidades

- **Instanciação Simbólica:** Substituição de matrizes de adjacência estáticas por objetos simbólicos lineares e reais.
- **Motor de Asserção (Injeção de Invariantes):** Validação matemática que impede a formação de sub-rotas disjuntas através da formulação MTZ.
- **Análise de Inviabilidade:** Diferenciação rigorosa entre cenários de caminhos válidos e provas matemáticas de segurança absoluta.
- **Ensaios de Estresse e Escalabilidade:** Protocolo experimental automatizado para medir o tempo de inferência e geração de conflitos conforme o grafo escala.

---

## Estrutura do Projeto

Estrutura de diretórios proposta para o ecossistema do verificador formal:
```bash
verificador_cps/
├── Cargo.toml (se houver wrappers) ou requirements.txt
├── config/
│   └── parametros_seguranca.json
├── logs/
│   └── analise_solver.log (gerado em runtime)
├── src/
│   ├── main.py
│   ├── modelagem_mtz.py
│   └── executor_simbolico.py
└── tests/
    └── test_casos_controle.py
```
## Bibliotecas e Ferramentas Utilizadas

### z3-solver
> Usado para:
- Instanciar variáveis simbólicas inteiras (`z3.Int()`) e reais (`z3.Real()`).
- Processar as cláusulas geradas pelas restrições físicas do grafo através da arquitetura DPLL($T$).
- Resolver as condições de caminho e gerar contraexemplos através do motor CDCL interno do solver da Microsoft Research.

### pytest
> Usado para:
- Automatizar os testes unitários do motor de asserção.
- Validar as matrizes base de controle de dimensões pequenas ($4 \times 4$ e $5 \times 5$).

### time & os
> Usado para:
- Monitorar o tempo exato de inferência do solver em milissegundos ($ms$).
- Gerenciar a persistência das métricas e relatórios de estresse computacional.

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
2. **Estudo de Complexidade dos Algoritmos do Z3:** Análise assintótica de pior caso do algoritmo CDCL para SAT, da arquitetura $\text{DPLL}(T)$ para teorias combinadas e das heurísticas de *E-matching* para quantificadores.

👉 [Acesse o Relatório Técnico / Artigo Completo](/relatorio/verificacao_formal_cps_logistica.pdf)

---

## Referências

- KING, James C. Symbolic execution and program testing. *Communications of the ACM*, vol. 19, n. 7, p. 385–394, 1976. DOI: 10.1145/360248.360252.

- DE MOURA, Leonardo; BJØRNER, Nikolaj. Z3: An efficient SMT solver. In: *International Conference on Tools and Algorithms for the Construction and Analysis of Systems*. Springer, Berlin, Heidelberg, 2008. p. 337-340.

- MILLER, Clair E.; TUCKER, Albert W.; ZEMLIN, Lowell A. Integer programming formulation of traveling salesman problems. *Journal of the ACM (JACM)*, vol. 7, n. 4, p. 326-329, 1960.
