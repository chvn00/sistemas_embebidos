# 02 — Semáforo Digital (simulado)
# Objetivos: modelar sistemas secuenciales con tiempos y estados.
# Retos: botón de peatón (simulado), tiempos configurables, log de ciclos.

import time

ESTADOS = [("🔴 Rojo", 3.0), ("🟡 Amarillo", 1.0), ("🟢 Verde", 3.0)]

def semaforo(ciclos=2):
    for c in range(ciclos):
        for nombre, t in ESTADOS:
            print(f"{nombre}  ({t}s)")
            time.sleep(t)

if __name__ == "__main__":
    semaforo(ciclos=2)
