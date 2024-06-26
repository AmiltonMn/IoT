from machine import Pin, PWM
import time

buzzer = PWM(Pin(12, Pin.OUT))
pir_sensor = Pin(13, Pin.IN)

def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty(512)
    time.sleep(0.5)
    buzzer.duty(0)
try:
    while True:
        valor = pir_sensor.value()
    
        if valor == 1:
            play_tone(440, 1)
            time.sleep(0.01)
            play_tone(1200, 1)
            time.sleep(0.01)
            play_tone(440, 1)
            time.sleep(0.01)
            play_tone(1200, 1)
            time.sleep(0.01)
finally:
    buzzer.deinit()
