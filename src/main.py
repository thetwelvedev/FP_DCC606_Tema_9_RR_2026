import random
import time
import z3

def simular_interdicao_simbolica(solver, d, x, n):
    """
    Injeta a possibilidade de QUALQUER aresta do sistema ser interditada.
    O Z3 tentará encontrar qual interdição específica quebra a segurança do software.
    """
    # 1. Criar uma matriz de variáveis booleanas para os bloqueios
    bloqueios = [[z3.Bool(f"bloqueio_{i}_{j}") for j in range(n)] for i in range(n)]
    
    # 2. Se a aresta i->j for interditada, o custo dela vai para 9999
    for i in range(n):
        for j in range(n):
            if i != j:
                # Se bloqueio for True, d[i][j] == 9999. Se for False, mantém a lógica original.
                solver.add(z3.Implies(bloqueios[i][j] == True, d[i][j] == 9999))
    
    # 3. Restrição Ciberfísica: Garantir que exatamente 1 aresta do grafo falhará
    # No Z3, True conta como 1 e False como 0 em somatórios se convertermos para Int
    total_bloqueios = z3.Sum([z3.If(bloqueios[i][j], 1, 0) for i in range(n) for j in range(n) if i != j])
    
    solver.add(total_bloqueios == 1)


def verificar_seguranca_tsp(n, matriz_base, custo_max_simbolico, restricoes_adicionais=None):
    solver = z3.Solver()
    
    # 1. Instanciação de Variáveis de Decisão do Caminho (X_ij)
    x = [[z3.Int(f"x_{i}_{j}") for j in range(n)] for i in range(n)]
    
    # 2. Instanciação de Variáveis Auxiliares de Ordem (u_i) para MTZ
    u = [z3.Int(f"u_{i}") for i in range(n)]
    
    # 3. Criação da Matriz de Distância Simbólica
    d = [[z3.Int(f"d_{i}_{j}") for j in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                solver.add(d[i][j] == 0)
                solver.add(x[i][j] == 0)
            else:
                if isinstance(matriz_base[i][j], int):
                    solver.add(d[i][j] == matriz_base[i][j])
                solver.add(d[i][j] >= 0)

    # 4. Restrições do Domínio das Variáveis de Decisão
    for i in range(n):
        for j in range(n):
            if i != j:
                solver.add(z3.Or(x[i][j] == 0, x[i][j] == 1))

    # 5. Invariantes de Roteamento (Cada nó visitado exatamente uma vez)
    for i in range(n):
        solver.add(z3.Sum([x[i][j] for j in range(n) if j != i]) == 1)
        solver.add(z3.Sum([x[j][i] for j in range(n) if j != i]) == 1)

    # 6. Eliminação de Sub-rotas (Formulação MTZ)
    for i in range(1, n):
        solver.add(u[i] >= 1)
        solver.add(u[i] <= n - 1)
        for j in range(1, n):
            if i != j:
                solver.add(u[i] - u[j] + n * x[i][j] <= n - 1)

    # 7. Cálculo do Custo Total da Rota
    custo_total = z3.Sum([d[i][j] * x[i][j] for i in range(n) for j in range(n)])
    
    # 8. Injeção do Limite de Segurança Parametrizado
    Cmax = z3.Int("Cmax")
    solver.add(Cmax == custo_max_simbolico)
    
    # Condição de Erro / Busca por Falhas
    solver.add(custo_total > Cmax)
    
    # Injeção de restrições de estresse dinâmico (se fornecidas)
    if restricoes_adicionais:
        restricoes_adicionais(solver, d, x, n)  

    # 9. Verificação e Métricas (CORRIGIDO PARA PYTHON 3.13)
    start_time = time.time()
    resultado = solver.check()
    execution_time_ms = (time.time() - start_time) * 1000
    
    num_clausulas = len(solver.assertions())
    
    # Tratamento seguro das estatísticas do Z3
    stats = solver.statistics()
    conflitos = 0
    for stat_name in ['conflicts', 'num conflicts', 'sat conflicts']:
        try:
            conflitos = stats.__getattr__(stat_name)
            break # Se achou, para o loop
        except AttributeError:
            continue

    return {
        "status": resultado,
        "tempo_ms": execution_time_ms,
        "clausulas": num_clausulas,
        "conflitos": conflitos,
        "model": solver.model() if resultado == z3.sat else None,
        "vars_x": x # Retorna a referência das variáveis para o parser
    }

def gerar_matriz_controle(n, min_dist=10, max_dist=50):
    """
    Gera uma matriz de adjacência simétrica de tamanho n x n para o TSP.
    A diagonal principal é preenchida com 0.
    """
    # Inicializa a matriz com zeros
    matriz = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            distancia = random.randint(min_dist, max_dist)
            matriz[i][j] = distancia
            matriz[j][i] = distancia  # Garante que o grafo é não-direcionado (simétrico)
            
    return matriz

def executar_ensaio_estresse(restricoes_adicionais=None):
    """
    Automatiza os testes para os tamanhos exigidos no relatório (4x4, 6x6, 8x8)
    e exibe os resultados formatados no padrão da Tabela 8.
    """
    # Tamanhos solicitados no protocolo de teste
    dimensoes = [4, 6, 8, 10, 12]
    
    print("-" * 80)
    print(f"{'Dimensão':<10} | {'Cláusulas':<10} | {'Resultado Z3':<15} | {'Tempo (ms)':<12} | {'Conflitos':<10}")
    print("-" * 80)
    
    for n in dimensoes:
        # 1. Gera o grafo de forma independente
        matriz_teste = gerar_matriz_controle(n)
        
        # 2. Define um teto de segurança arbitrário para testar o solver
        # Vamos colocar um teto baixo para forçar o Z3 a trabalhar procurando falhas (SAT)
        custo_max_seguranca = n * 80 
        
        # 3. Chama o verificador formal
        res = verificar_seguranca_tsp(
            n=n, 
            matriz_base=matriz_teste, 
            custo_max_simbolico=custo_max_seguranca,
            restricoes_adicionais=restricoes_adicionais
        )
        
        # 4. Formata o status para exibição (SAT / UNSAT / UNKNOWN)
        status_str = str(res["status"]).upper()
        
        # 5. Imprime a linha da tabela correspondente ao tamanho atual
        print(f"{n:<2} x {n:<2}   | {res['clausulas']:<10} | {status_str:<15} | {res['tempo_ms']:<12.2f} | {res['conflitos']:<10}")

# --- Execução do Caso de Controle ---
if __name__ == "__main__":
    # Define uma seed para que os resultados sejam reproduzíveis no relatório, se quiser
    random.seed(42)
    
    print("=== INICIANDO ENSAIO DE ESTRESSE COMPUTACIONAL (SMT SOLVER) ===")
    executar_ensaio_estresse(simular_interdicao_simbolica)
    print("-" * 80)