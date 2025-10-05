# -*- coding: utf-8 -*-
"""Web_Flask.ipynb

Objetivo general
Construir una aplicación web local que permita encender/apagar un LED y visualizar la distancia medida por un sensor ultrasónico HC-SR04 en tiempo real, usando Python, Flask y GPIO de la Raspberry Pi.

Materiales
1 Raspberry Pi (con Raspberry Pi OS con escritorio y Python 3)
1 LED + resistencia 220–330 Ω
1 sensor ultrasónico HC-SR04
Cables macho–macho y protoboard
(Opcional) un buzzer o segundo LED para alerta sonora/visual

Actualizar e instalar Flask:
sudo apt update
sudo apt install python3-flask -y

Crear una carpeta para el proyecto:
mkdir flask_gpio
cd flask_gpio

Abrir Thonny y guardar el archivo como app.py dentro de la carpeta.

Prueba:
Ejecutar el programa en Thonny (F5).
Abrir el navegador web en la Raspberry Pi o en otro dispositivo conectado a la misma red.

Escribe la dirección:
http://<tu_direccion_IP>:5000

(Consulta la IP con hostname -I en la terminal).
"""

# -------------------------------
# Proyecto: Panel Web GPIO + Flask
# -------------------------------

from flask import Flask, render_template_string, request, jsonify
import RPi.GPIO as GPIO
import time

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)
LED = 17
TRIG, ECHO = 23, 24

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Función para medir distancia
def distancia_cm():
    # Enviar pulso de disparo
    GPIO.output(TRIG, 0)
    time.sleep(0.0002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    # Esperar el eco
    t0 = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - t0 > 0.02:
            return None
    start = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() - start > 0.02:
            return None
    end = time.time()

    # Calcular distancia
    duracion = end - start
    distancia = (duracion * 34300) / 2  # cm
    return distancia

# Interfaz HTML incrustada
HTML = """
<!doctype html>
<html>
<head>
<title>Panel GPIO</title>
<meta charset="utf-8">
<style>
body { font-family: Arial; background: #f2f2f2; text-align: center; }
button { padding: 10px 20px; margin: 10px; font-size: 16px; }
#dist { font-size: 20px; margin-top: 20px; color: #333; }
</style>
</head>
<body>
<h2>🔹 Panel de Control Raspberry Pi 🔹</h2>
<button onclick="fetch('/led?state=on')">Encender LED</button>
<button onclick="fetch('/led?state=off')">Apagar LED</button>
<p id="dist">Distancia: -- cm</p>
<script>
async function actualizarDistancia(){
  const resp = await fetch('/dist');
  const data = await resp.json();
  document.getElementById('dist').innerText =
    data.dist ? "Distancia: " + data.dist.toFixed(1) + " cm" : "Distancia: --";
}
setInterval(actualizarDistancia, 500);
</script>
</body>
</html>
"""

# Crear aplicación Flask
app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/led")
def led_control():
    state = request.args.get("state", "off")
    GPIO.output(LED, GPIO.HIGH if state == "on" else GPIO.LOW)
    return ("", 204)

@app.route("/dist")
def dist_read():
    d = distancia_cm()
    return jsonify({"dist": d})

try:
    print("Servidor ejecutándose en http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)
finally:
    GPIO.cleanup()
