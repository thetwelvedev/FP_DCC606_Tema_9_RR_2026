import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# cria pasta se não existir
Path("resultados").mkdir(exist_ok=True)

# leitura dos resultados
df = pd.read_csv("resultados/resultados.csv")

# ==========================
# GRÁFICO TEMPO
# ==========================

plt.figure(figsize=(8,5))
plt.plot(df["n"], df["tempo_ms"], marker="o")
plt.title("Tempo de Execução x Número de Cidades")
plt.xlabel("Número de cidades")
plt.ylabel("Tempo (ms)")
plt.grid(True)

plt.savefig(
    "resultados/grafico_tempo.png",
    bbox_inches="tight"
)

plt.close()

# ==========================
# GRÁFICO CLÁUSULAS
# ==========================

plt.figure(figsize=(8,5))
plt.plot(df["n"], df["clausulas"], marker="o")
plt.title("Número de Cláusulas x Número de Cidades")
plt.xlabel("Número de cidades")
plt.ylabel("Quantidade de cláusulas")
plt.grid(True)

plt.savefig(
    "resultados/grafico_clausulas.png",
    bbox_inches="tight"
)

plt.close()

# ==========================
# GRÁFICO CONFLITOS
# ==========================

plt.figure(figsize=(8,5))
plt.plot(df["n"], df["conflitos"], marker="o")
plt.title("Conflitos do Solver x Número de Cidades")
plt.xlabel("Número de cidades")
plt.ylabel("Conflitos")
plt.grid(True)

plt.savefig(
    "resultados/grafico_conflitos.png",
    bbox_inches="tight"
)

plt.close()

print("Gráficos gerados com sucesso!")