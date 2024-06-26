from machine import Pin
import time
import dht
import urequests
import ujson
import network

dht_sensor = dht.DHT11(Pin(33))
R_button = Pin(35, Pin.IN)
B_button = Pin(34, Pin.IN)
R_led = Pin(14, Pin.OUT)
B_led = Pin(32, Pin.OUT)
R_button2 = Pin(26, Pin.IN)
B_button2 = Pin(12, Pin.IN)
R_led2 = Pin(13, Pin.OUT)
B_led2 = Pin(27, Pin.OUT)
TV_button = Pin(25, Pin.IN)
color = 0
color2 = 0
lightOn = 0
lightOn2 = 0
TV_value = 0


nome = "Wifi Amilton"
senha = "87654321"

FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/"
SECRET_KEY = ""

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
    url = FIREBASE_URL + "Amilton.json"

    response = urequests.put(url, data=ujson.dumps(data), headers=headers)
    print("Firebase Response:", response.text)
    response.close()
    
def get():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + SECRET_KEY}

    url = FIREBASE_URL + "/Amilton.json"  # Adjust path as per your database structure
    response = urequests.get(url, headers=headers)

    if response.status_code == 200:
        data = ujson.loads(response.text)
        print("Firebase Response:", data)
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

    response.close()
    
conectarWifi()
        
while True:
    
    data = get()

    R_value = R_button.value()
    B_value = B_button.value()
    R_value2 = R_button2.value()
    B_value2 = B_button2.value()
    
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()
    
    R_value = data['principalLigt']
    
    if R_value == 1:
        if color != 2:
            if R_led.value() == 0:
                R_led.on()
                color = 1
                lightOn = 1
            else:
                R_led.off()
                color = 0
                lightOn = 0
            
    if B_value == 1:
        if color != 1:
            if B_led.value() == 0:
                B_led.on()
                color = 2
                lightOn = 1
            else:
                B_led.off()
                color = 0
                lightOn = 0
                
    if R_value2 == 1:
        if color2 != 2:
            if R_led2.value() == 0:
                R_led2.on()
                color2 = 1
                lightOn2 = 1
            else:
                R_led2.off()
                color2 = 0
                lightOn2 = 0
            
    if B_value2 == 1:
        if color2 != 1:
            if B_led2.value() == 0:
                B_led2.on()
                color2 = 2
                lightOn2 = 1
            else:
                B_led2.off()
                color2 = 0
                lightOn2 = 0
                
    if TV_button.value() == 1:
        if TV_value == 0:
            TV_value = 1
        else:
            TV_value = 0
    
    
    info = {
        
        "LED1" : {
            "Temperatura" : temp,
            "Umidade" : hum,
            "color" : color,
            "principalLight" : lightOn,
            "Tv" : TV_value,
        },
        
        "LED2" : {
            "Temperatura" : temp,
            "Umidade" : hum,
            "color" : color2,
            "principalLight" : lightOn2,
            "Tv" : TV_value,
        }
    }
    enviarFire(info)
    
    