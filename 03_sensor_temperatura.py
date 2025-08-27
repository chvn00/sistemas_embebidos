# 03 — Sensor de Temperatura (simulado)
# Objetivos: generar datos de sensor, tomar decisiones con umbrales, graficar series.

import random, time
import pandas as pd
import matplotlib.pyplot as plt

def simular_temperatura(n=30, mu=26.0, amp=4.0):
    return [mu + random.uniform(-amp, amp) for _ in range(n)]

def main():
    T = simular_temperatura(n=40)
    UMBRAL = 27.0
    log = []
    for i, t in enumerate(T):
        estado = "VENTILADOR ON 🌀" if t > UMBRAL else "VENTILADOR OFF"
        log.append({"t": i, "temp": t, "fan": 1 if t > UMBRAL else 0})
        print(f"[{i:02d}] T={t:.2f}°C -> {estado}")
        time.sleep(0.02)

    df = pd.DataFrame(log)
    plt.figure()
    plt.plot(df["t"], df["temp"])
    plt.axhline(UMBRAL)
    plt.title("Temperatura simulada")
    plt.xlabel("Tiempo (pasos)"); plt.ylabel("°C")
    plt.show()

if __name__ == "__main__":
    main()
