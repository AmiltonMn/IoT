import urequests
import ujson
import network
from machine import Pin
import dht
import time

nome = "Celofone da Sasá"
senha = "sasa12345"

FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/"
SECRET_KEY = ""

dht_sensor = dht.DHT11(Pin(27))

def read_dht11():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print(f"Temperatura: {temp}°C. Umidade: {hum}")
    except OSError as e:
        print("Falha na leitura do sensor:", e)
    time.sleep(2)
        
def conectarWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando no WiFi...")
        wlan.connect(nome, senha)
        while not wlan.isconnected():
            pass
    print("Wifi conectado... IP: {}".format(wlan.ifconfig()[0]))

def enviarFire(data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + SECRET_KEY
    }
    url = FIREBASE_URL + "/Amilton.json"  # Coloque o seu nome

    response = urequests.put(url, data=ujson.dumps(data), headers=headers)
    print("Firebase Response:", response.text)
    response.close()


conectarWifi()

while True:
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()
    print(f"Temperatura: {temp}°C. Umidade: {hum}")
    time.sleep(1)
    informacao = {
        "Temperatura:":temp,
        "Umidade:":hum,
    }
    enviarFire(informacao)
    time.sleep(1)
