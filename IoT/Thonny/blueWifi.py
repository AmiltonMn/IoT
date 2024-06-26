import ublue
import _thread
import time
import urequests
import ujson
import network
from machine import Pin

FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/"
SECRET_KEY = ""

#Dê um nome para o seu bluetooth
nome = "Amilton BLE"

#Seta o pino do led 
led = Pin(27, Pin.OUT)

#Função obrigatória para iniciar o funcionamento do bluetooth
def funcaoA():
    ublue.ublueON(nome)

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
    url = FIREBASE_URL + "/NOME.json"  # Coloque o seu nome

    response = urequests.put(url, data=ujson.dumps(data), headers=headers)
    print("Firebase Response:", response.text)
    response.close()

def funcaoB(informacao):
    while True:
        try:
            print(ublue.info)
            if (int(ublue.info) == 0): #Lógica invertida pois nessa esp32 usa-se o pull_up
                led.value(1)
                informacao = "Ligado"
                enviarFire(informacao)
            elif (int(ublue.info) == 1):
                led.value(0)
                informacao = "Desligado"
                enviarFire(informacao)
        except ValueError:
            print("Entre com um valor inteiro")
            ublue.info = 0
        time.sleep(1)

#Inicia o processamento em 2 núcleos simultaneamente (multithreading)
_thread.start_new_thread(funcaoA,())
_thread.start_new_thread(funcaoB,())
