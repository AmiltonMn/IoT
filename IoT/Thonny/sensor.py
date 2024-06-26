from machine import Pin
import time

pir_sensor = Pin(34, Pin.IN)

def read_pir_sensor():
    while True:
        if pir_sensor.value() == 1:
            print("Movimento Perto")
        else:
            print("Nenhum movimento.")
            
        time.sleep(1)
read_pir_sensor()
            