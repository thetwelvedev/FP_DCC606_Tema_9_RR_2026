import random
from modelagem_mtz import verificar_seguranca_tsp

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

def executar_ensaio_estresse(usar_interdicao=False, restricoes_adicionais=None):
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
            usar_interdicao=usar_interdicao,
            restricoes_adicionais=restricoes_adicionais
        )
        
        # 4. Formata o status para exibição (SAT / UNSAT / UNKNOWN)
        status_str = str(res["status"]).upper()
        
        # 5. Imprime a linha da tabela correspondente ao tamanho atual
        print(f"{n:<2} x {n:<2}   | {res['clausulas']:<10} | {status_str:<15} | {res['tempo_ms']:<12.2f} | {res['conflitos']:<10}")
