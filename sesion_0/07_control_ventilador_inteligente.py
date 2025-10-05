# 07 — Controlador de Ventilador Inteligente (simulado)
# Objetivos: diseñar reglas discretas y mapear entradas a modos de actuador.

import random
import pandas as pd
import matplotlib.pyplot as plt

def modo_ventilador(temp):
    if temp < 25: return 0   # off
    if temp < 28: return 50  # medio
    return 100               # alto

def main():
    temps = [24 + random.uniform(-2, 6) for _ in range(60)]
    modes = [modo_ventilador(t) for t in temps]

    df = pd.DataFrame({"t": range(len(temps)), "temp": temps, "duty": modes})
    print(df.head())

    plt.figure(); plt.plot(df["t"], df["temp"]); plt.title("Temperatura"); plt.xlabel("t"); plt.ylabel("°C"); plt.show()
    plt.figure(); plt.plot(df["t"], df["duty"]); plt.title("Duty ventilador (%)"); plt.xlabel("t"); plt.ylabel("%"); plt.show()

if __name__ == "__main__":
    main()
