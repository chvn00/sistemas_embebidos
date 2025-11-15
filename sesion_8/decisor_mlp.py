# -*- coding: utf-8 -*-
"""Decisor_MLP.ipynb

"""

sudo apt install python3-numpy -y

"""# Sistemas Embebidos
# Profesor: Cesar Hernando Valencia Niño

'''
# MLP embebido en Raspberry Pi con entradas desde DIP switch y salida en LEDs

Descripción del problema
------------------------
Este programa implementa en la Raspberry Pi la fase de INFERENCIA de una red
neuronal multicapa (MLP) previamente entrenada en Google Colab.

La idea es simular un sistema industrial sencillo donde 4 condiciones binarias
(señaladas mediante un DIP switch de 4 posiciones) describen el estado del
proceso. Estas 4 entradas se interpretan como un vector:

    x = [x1, x2, x3, x4]   con xi ∈ {0, 1}

A partir de estas entradas, un modelo MLP toma una decisión de clasificación
entre tres posibles estados:

    - Clase 0: ESTADO NORMAL
    - Clase 1: ESTADO DE ADVERTENCIA
    - Clase 2: ESTADO CRÍTICO

La red neuronal (W1, b1, W2, b2) fue entrenada en un cuaderno de Google Colab
con un conjunto de datos sintético. Los pesos resultantes se copiaron aquí
como constantes de NumPy. En este script NO se entrena la red, únicamente se
usa para calcular la salida (inferencia) en tiempo real.

Según la clase predicha, se encienden los siguientes LEDs:

    - Clase 0 (NORMAL): LED verde encendido
    - Clase 1 (ADVERTENCIA): LED amarillo encendido
    - Clase 2 (CRÍTICO): LED rojo encendido (o parpadeando)

Suma de bits ≤ 1 → Clase 0 = NORMAL → LED verde
Suma de bits = 2 → Clase 1 = ADVERTENCIA → LED amarillo
Suma de bits ≥ 3 → Clase 2 = CRÍTICO → LED rojo

Configuración de hardware en la Raspberry Pi
--------------------------------------------
- DIP switch de 4 posiciones:
    Cada switch se conecta entre un pin GPIO y 3.3 V, usando resistencias
    de pull-down (externas o internas). En este ejemplo se usan los pines:

        SW1 -> GPIO 5
        SW2 -> GPIO 6
        SW3 -> GPIO 13
        SW4 -> GPIO 19

    Cuando el switch está en ON, el GPIO lee un '1'; cuando está en OFF, lee '0'.

- LEDs de salida:
    Se utilizan tres LEDs para indicar el estado del sistema:

        LED verde  -> GPIO 17  (estado NORMAL)
        LED amarillo -> GPIO 27 (estado de ADVERTENCIA)
        LED rojo   -> GPIO 22  (estado CRÍTICO)

    Cada LED debe conectarse con su respectiva resistencia limitadora de corriente,
    con el cátodo a GND y el ánodo al pin GPIO a través de la resistencia.

Requisitos de software
----------------------
- Sistema operativo Raspberry Pi OS con soporte de Python 3.
- Librerías instaladas:
    - RPi.GPIO  (manejo de pines GPIO)
    - NumPy     (operaciones matriciales del MLP)

  Para instalar NumPy (si no está):
      sudo apt update
      sudo apt install python3-numpy -y

Modo de uso
-----------
1. Conectar el DIP switch y los LEDs según la configuración anterior.
2. Copiar en este archivo los pesos entrenados W1, b1, W2 y b2 obtenidos desde el
   cuaderno de Google Colab (sustituir los valores de ejemplo por los reales).
3. Ejecutar este script en la Raspberry Pi desde Thonny o terminal:

       python3 mlp_embebido.py

4. Cambiar manualmente las posiciones del DIP switch. El programa:
    - Leerá el vector de entrada x = [x1, x2, x3, x4].
    - Aplicará el modelo MLP (capa oculta + capa de salida).
    - Seleccionará la clase de mayor score (argmax).
    - Encenderá el LED correspondiente (verde, amarillo o rojo).


'''

"""

import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BCM)

# Pines DIP switch
SW_PINS = [5, 6, 13, 19]   # x1, x2, x3, x4
for p in SW_PINS:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Pines LEDs
LED_VERDE  = 17
LED_AMAR   = 27
LED_ROJO   = 22
for p in [LED_VERDE, LED_AMAR, LED_ROJO]:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

# ========= PESOS ENTRENADOS (EJEMPLO, SUSTITUIR CON LOS REALES) =========
# Copiar aquí los pesos desde Colab:


# =======================================================================

def leer_entradas():
    """Lee el DIP switch y devuelve vector x de 4 bits (0/1) como numpy array float."""
    valores = [GPIO.input(p) for p in SW_PINS]  # lista con 0/1
    return np.array(valores, dtype=float)

def mlp_forward(x):
    """
    x: vector (4,)
    Devuelve la clase predicha (0,1,2) y los logits.
    MLP: capa oculta (ReLU), capa de salida (argmax).
    """
    # Capa oculta: z1 = ReLU(W1^T x + b1)
    # Nota: W1: (4, 4) si lo dejamos como [in, hidden]
    # hacemos: hidden = ReLU(x @ W1 + b1)
    z1 = np.maximum(0, x @ W1 + b1)   # ReLU

    # Capa salida: z2 = W2^T z1 + b2   (z2: (3,))
    logits = z1 @ W2 + b2

    # Predicción = índice del máximo
    clase = int(np.argmax(logits))
    return clase, logits

def mostrar_clase(clase):
    """Enciende los LEDs según la clase."""
    if clase == 0:
        # NORMAL → solo verde
        GPIO.output(LED_VERDE, 1)
        GPIO.output(LED_AMAR,  0)
        GPIO.output(LED_ROJO,  0)
    elif clase == 1:
        # ADVERTENCIA → amarillo
        GPIO.output(LED_VERDE, 0)
        GPIO.output(LED_AMAR,  1)
        GPIO.output(LED_ROJO,  0)
    else:
        # CRÍTICO → rojo parpadeante
        GPIO.output(LED_VERDE, 0)
        GPIO.output(LED_AMAR,  0)
        GPIO.output(LED_ROJO,  1)
        time.sleep(0.2)
        GPIO.output(LED_ROJO, 0)
        time.sleep(0.2)

try:
    print("MLP embebido con DIP switch. Ctrl+C para salir.")
    while True:
        x = leer_entradas()
        clase, logits = mlp_forward(x)

        print(f"Entradas DIP: {x.astype(int)} -> Clase: {clase}, logits: {np.round(logits,2)}", end="\r")

        if clase in [0,1]:
            mostrar_clase(clase)
            time.sleep(0.3)
        else:
            # Para clase crítica, dejamos que la función maneje el parpadeo
            mostrar_clase(clase)

except KeyboardInterrupt:
    print("\nSaliendo...")
finally:
    GPIO.output(LED_VERDE, 0)
    GPIO.output(LED_AMAR,  0)
    GPIO.output(LED_ROJO,  0)
    GPIO.cleanup()
