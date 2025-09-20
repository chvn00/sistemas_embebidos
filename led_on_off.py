# -*- coding: utf-8 -*-

# Importar librerías necesarias
import RPi.GPIO as GPIO
import time

# Usar numeración BCM de los pines
GPIO.setmode(GPIO.BCM)

# Configurar el pin GPIO 17 como salida
GPIO.setup(17, GPIO.OUT)

# Encender y apagar el LED 5 veces
for i in range(5):
    GPIO.output(17, GPIO.HIGH)  # LED encendido
    time.sleep(1)               # Esperar 1 segundo
    GPIO.output(17, GPIO.LOW)   # LED apagado
    time.sleep(1)

# Liberar los pines al finalizar
GPIO.cleanup()
