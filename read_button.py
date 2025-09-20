# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Pin 18 como entrada (botón), con resistencia interna pull-down
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(18) == GPIO.HIGH:
        print("¡Botón presionado!")
    else:
        print("Botón no presionado")
    time.sleep(0.5)  # Pausa para evitar lecturas muy rápidas
