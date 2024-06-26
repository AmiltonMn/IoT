from machine import Pin
import time
import dht

dht_sensor = dht.DHT11(Pin(27))

def read_dht11():
    
    while True:
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
            print(f"Temperatura: {temp}°C. Umidade: {hum}")
        except OSError as e:
            print("Falha na leitura do sensor:", e)
        
        time.sleep(2)
        
read_dht11()