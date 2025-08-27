# 06 — Mini-Estación de Monitoreo (simulada)
# Objetivos: integrar lecturas múltiples, tabular y graficar.

import random
import pandas as pd
import matplotlib.pyplot as plt

def leer_sensores(n=60):
    datos = []
    for i in range(n):
        T = 24 + random.uniform(-3, 3)
        H = 60 + random.uniform(-10, 10)
        L = 500 + random.uniform(-200, 200)
        datos.append({"t": i, "temp": T, "hum": H, "lux": L})
    return pd.DataFrame(datos)

def main():
    df = leer_sensores(60)
    print(df.head())

    plt.figure(); plt.plot(df["t"], df["temp"]); plt.title("Temperatura"); plt.xlabel("t"); plt.ylabel("°C"); plt.show()
    plt.figure(); plt.plot(df["t"], df["hum"]);  plt.title("Humedad");     plt.xlabel("t"); plt.ylabel("%");  plt.show()
    plt.figure(); plt.plot(df["t"], df["lux"]);  plt.title("Luz");         plt.xlabel("t"); plt.ylabel("Lux (sim)"); plt.show()

if __name__ == "__main__":
    main()
