# 08 — Juego de Reflejos (tiempo de reacción)
# Objetivos: interacción con el usuario y medición de tiempos.

import time, random, statistics

def ronda():
    espera = random.uniform(1.0, 3.0)
    print("Prepárate...")
    time.sleep(espera)
    t0 = time.time()
    input("¡YA! Presiona ENTER lo más rápido posible... ")
    return (time.time() - t0)*1000  # ms

def main():
    tiempos = []
    for i in range(3):
        ms = ronda()
        tiempos.append(ms)
        print(f"Tiempo: {ms:.1f} ms")

    if len(tiempos) > 1:
        print(f"Promedio: {statistics.mean(tiempos):.1f} ms | Desv: {statistics.pstdev(tiempos):.1f} ms")

if __name__ == "__main__":
    main()
