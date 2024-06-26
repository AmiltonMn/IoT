import machine
import time

# led = machine.Pin(23, machine.Pin.OUT)

# while True:
#   led.value(not led.value())
#   time.sleep(1)

led = machine.Pin(18, machine.Pin.OUT)
led2 = machine.Pin(19, machine.Pin.OUT)
button = machine.Pin(4, machine.Pin.IN)
button2 = machine.Pin(2, machine.Pin.IN)


while True:
    button_state = button.value()
    button2_state = button2.value()
    
    if button_state == 1:
        print("Ligando LED 1")
        led.on()
        time.sleep(1)
    else:
        led.off()
    
    if button2_state == 1:
        print("Ligando LED 2")
        led2.on()
        time.sleep(1)
    else:
        led2.off()

    print("Carregando próxima ação...")
    time.sleep(2)