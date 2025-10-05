# -*- coding: utf-8 -*-
"""Monitoreo_iot.ipynb

Objetivo
Aprender a enviar datos de sensores de la Raspberry Pi a la nube (ThingSpeak) para visualizarlos en tiempo real mediante gráficos web, combinando conceptos de sistemas embebidos e Internet de las Cosas (IoT).

Materiales:
Raspberry Pi con acceso a internet
Sensor HC-SR04 (o DHT11 si prefieres temperatura/humedad)
Cables y protoboard
Cuenta gratuita en ThingSpeak.com

Conceptos que se refuerzan:
Comunicación entre hardware y servicios en la nube
API REST (envío de datos con peticiones HTTP)
JSON, claves de API y almacenamiento remoto
Integración entre Python, Flask y un servicio IoT

Flujo del proyecto:
La Raspberry Pi mide distancia.
Cada cierto tiempo (por ejemplo, 15 segundos) envía el dato a ThingSpeak por internet.
En ThingSpeak, se generan gráficas en tiempo real que pueden verse desde cualquier navegador o celular.

Pasos básicos

Crear una cuenta gratuita en ThingSpeak.com
Crear un nuevo canal y activa al menos un Field (campo).
Copiar Write API Key (clave para enviar datos).

En Raspberry Pi, instala las librerías necesarias:
sudo apt update
sudo apt install python3-requests -y
"""

# --------------------------------------------
# Envío de datos de Raspberry Pi a ThingSpeak
# Sensor: HC-SR04 (distancia en cm)
# --------------------------------------------

import RPi.GPIO as GPIO
import time, requests

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
TRIG, ECHO = 23, 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Tu clave de escritura de ThingSpeak
API_KEY = "TU_API_KEY_AQUI"

def medir_distancia():
    GPIO.output(TRIG, 0)
    time.sleep(0.0002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        end = time.time()

    duracion = end - start
    distancia = (duracion * 34300) / 2
    return round(distancia, 2)

try:
    while True:
        dist = medir_distancia()
        print(f"Distancia medida: {dist} cm")

        # Enviar a ThingSpeak
        url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={dist}"
        response = requests.get(url)
        if response.status_code == 200:
            print("Dato enviado correctamente ✅")
        else:
            print("Error al enviar ❌")

        time.sleep(15)  # enviar cada 15 segundos

except KeyboardInterrupt:
    print("\nFinalizando programa...")
finally:
    GPIO.cleanup()
