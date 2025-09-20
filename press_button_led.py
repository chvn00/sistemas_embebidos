# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# LED en GPIO17, Botón en GPIO18
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(18) == GPIO.HIGH:   # Si el botón está presionado
        GPIO.output(17, GPIO.HIGH)    # Encender LED
    else:
        GPIO.output(17, GPIO.LOW)     # Apagar LED
    time.sleep(0.1)  # Pequeña pausa para estabilidad
