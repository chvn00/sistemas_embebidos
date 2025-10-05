# 01 — Blink Virtual (LED simulado)
# Fecha: 2025-08-27
# Objetivos:
# - Entender salidas digitales ON/OFF.
# - Controlar tiempos de encendido/apagado.
# Retos:
# - R1: patrón SOS en Morse.
# - R2: Secuencia ON:OFF desde input().
# - R3: Registrar timestamps y graficar duty efectivo.

import time

def blink(ciclos=10, on_ms=500, off_ms=500):
    for i in range(ciclos):
        print("LED ON 💡")
        time.sleep(on_ms/1000)
        print("LED OFF ⚫")
        time.sleep(off_ms/1000)

if __name__ == "__main__":
    blink(ciclos=5, on_ms=300, off_ms=300)
