import random
from executor_simbolico import executar_ensaio_estresse
from modelagem_mtz import simular_restricao_energia_cps

# --- Execução do Caso de Controle ---
if __name__ == "__main__":
    # Define uma seed para que os resultados sejam reproduzíveis no relatório, se quiser
    random.seed(42)
    
    print("=== INICIANDO ENSAIO DE ESTRESSE COMPUTACIONAL (SMT SOLVER) ===")
    #executar_ensaio_estresse(usar_interdicao=True, restricoes_adicionais=simular_restricao_energia_cps)
    #executar_ensaio_estresse(usar_interdicao=False, restricoes_adicionais=simular_restricao_energia_cps)
    executar_ensaio_estresse(usar_interdicao=False, restricoes_adicionais=None)
    print("-" * 80)