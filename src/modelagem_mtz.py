import time
import z3

def verificar_seguranca_tsp(n, matriz_base, custo_max_simbolico, usar_interdicao=False, restricoes_adicionais=None):
    solver = z3.Solver()
    
    # 1. Instanciação de Variáveis de Decisão do Caminho (X_ij)
    x = [[z3.Int(f"x_{i}_{j}") for j in range(n)] for i in range(n)]
    
    # 2. Instanciação de Variáveis Auxiliares de Ordem (u_i) para MTZ
    u = [z3.Int(f"u_{i}") for i in range(n)]
    
    # 3. Criação da Matriz de Distância Simbólica
    d = [[z3.Int(f"d_{i}_{j}") for j in range(n)] for i in range(n)]

    if usar_interdicao:
        bloqueios = [[z3.Bool(f"bloqueio_{i}_{j}") for j in range(n)] for i in range(n)]
        # Garante que exatamente 1 aresta falhará no grafo todo
        total_bloqueios = z3.Sum([z3.If(bloqueios[i][j], 1, 0) for i in range(n) for j in range(n) if i != j])
        solver.add(total_bloqueios == 1)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                solver.add(d[i][j] == 0)
                solver.add(x[i][j] == 0)
            else:
                if isinstance(matriz_base[i][j], int):
                    if restricoes_adicionais:
                        # LEITURA: Se estiver bloqueado, o custo vira 9999. 
                        # Se NÃO estiver bloqueado, assume o valor original da matriz.
                        solver.add(d[i][j] == z3.If(bloqueios[i][j], 9999, matriz_base[i][j]))
                    else:
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
