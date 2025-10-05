# 04 — Control de Nivel de Agua (simulado)
# Objetivos: control ON/OFF (bang-bang) con perturbaciones.

import random
import matplotlib.pyplot as plt

def main():
    Lmin, Lmax = 40.0, 60.0
    nivel = 50.0
    hist_nivel, hist_bomba = [], []

    for t in range(120):
        ruido = random.uniform(-1.0, 1.0)
        nivel += ruido

        bomba_on = 0
        if nivel < Lmin:
            bomba_on = 1
        elif nivel > Lmax:
            bomba_on = 0

        if bomba_on:
            nivel += 1.5

        hist_nivel.append(nivel)
        hist_bomba.append(bomba_on)

    plt.figure()
    plt.plot(hist_nivel, label="Nivel")
    plt.axhline(Lmin, linestyle="--")
    plt.axhline(Lmax, linestyle="--")
    plt.title("Nivel de agua (simulación)")
    plt.xlabel("Tiempo"); plt.ylabel("Nivel")
    plt.legend(); plt.show()

if __name__ == "__main__":
    main()
