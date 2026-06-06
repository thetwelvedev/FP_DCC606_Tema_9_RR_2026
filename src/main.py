import random
from executor_simbolico import executar_ensaio_estresse

# --- Execução do Caso de Controle ---
if __name__ == "__main__":
    # Define uma seed para que os resultados sejam reproduzíveis no relatório, se quiser
    random.seed(42)
    
    print("=== INICIANDO ENSAIO DE ESTRESSE COMPUTACIONAL (SMT SOLVER) ===")
    executar_ensaio_estresse(usar_interdicao=True)
    print("-" * 80)