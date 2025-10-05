# 05 — PWM (modulación de ancho de pulso) simulado
# Objetivos: entender duty cycle, visualizar PWM.

import numpy as np
import matplotlib.pyplot as plt

def pwm_signal(t, dc=0.5):
    return (t % 1) < dc

def main():
    t = np.linspace(0, 1, 500)
    plt.figure()
    for dc in [0.2, 0.5, 0.8]:
        y = pwm_signal(t, dc=dc).astype(int)
        plt.plot(t, y, label=f"DC={int(dc*100)}%")
    plt.legend()
    plt.title("Señales PWM simuladas")
    plt.xlabel("Tiempo (s)"); plt.ylabel("Nivel lógico")
    plt.show()

if __name__ == "__main__":
    main()
