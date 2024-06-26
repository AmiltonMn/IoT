import urequests
import ujson
import network
from machine import Pin, PWM
import random
import time

led_Y = Pin(25, Pin.OUT)
led_R = Pin(26, Pin.OUT)
led_G = Pin(14, Pin.OUT)
led_B = Pin(27, Pin.OUT)
button_Y = Pin(34, Pin.IN)
button_R = Pin(35, Pin.IN)
button_G = Pin(32, Pin.IN)
button_B = Pin(33, Pin.IN)
buzzer = PWM(Pin(13, Pin.OUT))

pontos = 0
erro = 0
leds = 0
list_Game = []
list_User = []

led_Y.off()
led_R.off()
led_B.off()
led_G.off()

notes_freq = {
    'C4': 261, 'D4': 294, 'E4': 329, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 493,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 987,
    'REST': 0
}

def play_mario_death_sound():
    melody = [
        ('C5', 100), ('REST', 50), ('C5', 100), ('REST', 50), ('C5', 100),
        ('REST', 50), ('G4', 100), ('REST', 50), ('E4', 100), ('REST', 50),
        ('A4', 100), ('REST', 50), ('B4', 100)
    ]
    
    for note, duration in melody:
        if note != 'REST':
            buzzer.freq(notes_freq[note])
            buzzer.duty(50)  # ajuste o duty cycle conforme necessário para o volume desejado
        time.sleep_ms(duration)
        buzzer.duty(0)
        time.sleep_ms(50)  # pausa entre as notas
    
def play_mario_level_clear():
    melody = [
        ('E5', 225), ('E5', 225), ('REST', 100), ('C5', 225), ('E5', 225),
        ('G5', 225), ('G4', 225), ('REST', 100), ('G4', 100), ('C5', 100)
    ]
    
    for note, duration in melody:
        if note != 'REST':
            buzzer.freq(notes_freq[note])
            buzzer.duty(70)  # ajuste o duty cycle conforme necessário para o volume desejado
        time.sleep_ms(duration)
        buzzer.duty(0)
        time.sleep_ms(50)  # pausa entre as notas
        
        
# Função para tocar a nota no buzzer
def play_noteMusic(note, duration):
    if note != 'REST':
        buzzer.freq(notes_freq[note])
        buzzer.duty(50)  # ajuste o duty cycle conforme necessário para o volume desejado
    time.sleep_ms(duration)
    buzzer.duty(0)
    time.sleep_ms(50)  # pausa entre as notas
    
nome = "Wifi Amilton"
senha = "87654321"

FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/Amilton.json"
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
    
# Função de enviar para o FireBase a informação que desejar
def enviarFire(data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + SECRET_KEY
    }

    response = urequests.put(FIREBASE_URL, data=ujson.dumps(data), headers=headers)
    print("Firebase Response:", response.text)
    response.close()

def play_tone(freq, duration_ms):
    buzzer.freq(freq)  # Define a frequência em Hz
    buzzer.duty(70)    # Define o ciclo de trabalho (50% para som contínuo)
    time.sleep_ms(duration_ms)
    buzzer.duty(0)     # Para o som
    
# Função de validação de jogadas
def conferir_Jogada(i, pontos, erro):
        if list_User[i] != list_Game[i]: # Verifica se o valor da lista do jogador na posição i é diferente ao da sequência correta
            print("Game Over!")
            print(f"Você fez {pontos} pontos")
            return 1
        else:
            return 0
            pass
        
def erroJogador():
    play_mario_death_sound()
    
def proxNivel():
    play_mario_level_clear()

pontos = 0
conectarWifi()
buzzer.deinit()
nome = input("Digite seu nome:")
time.sleep(2)
buzzer.init()

while erro != 1:

    leds = random.randint(1, 4) # Gera um numero aleatório de 1 a 4 para escolher qual led será acesa
    list_Game.append(leds) # Adiciona o número à sequência
    
    # Acende as LED's de acordo com a sequência da lista
    
    for i in range(len(list_Game)):
        if list_Game[i] == 1:
            led_Y.on()
            play_tone(500, 500)
            time.sleep(0.2)
            led_Y.off()
            time.sleep(0.1)
            
        elif list_Game[i] == 2:
            led_R.on()
            play_tone(400, 500)
            time.sleep(0.2)
            led_R.off()
            time.sleep(0.1)
            
        elif list_Game[i] == 3:
            led_G.on()
            play_tone(350, 500)
            time.sleep(0.2)
            led_G.off()
            time.sleep(0.1)
            
        elif list_Game[i] == 4:
            led_B.on()
            play_tone(300, 500)
            time.sleep(0.2)
            led_B.off()
            time.sleep(0.1)
            
        time.sleep(0.2)
        
        if erro == 1:
            break
    
    list_User = []
    i = -1
    
    # Roda as jogados do jogador até que a sequência de jogadas tenha o mesmo tamanho que a sequência correta
    while len(list_User) < len(list_Game):
        time.sleep(0.1)
        value_Y = button_Y.value()
        value_R = button_R.value() 
        value_G = button_G.value()
        value_B = button_B.value()
        
        # Lê qual dos botões foi pressionado
        
        if value_Y == 1:
            play_tone(500, 500) 
            
            led_Y.on()
            time.sleep(0.2)
            led_Y.off()
            time.sleep(0.1)
            list_User.append(1)
            i += 1
            
            erro = conferir_Jogada(i, pontos, erro) # Validação da jogada do jogador. A variável erro recebe esse valor para poder parar o jogo, se retornar 1 o jogo acaba
            
        elif value_R == 1:
            led_R.on()
            play_tone(400, 500)
            time.sleep(0.2)
            led_R.off()
            time.sleep(0.1)
            list_User.append(2)
            i += 1
            erro = conferir_Jogada(i, pontos, erro)
            
        elif value_B == 1:
            led_G.on()
            play_tone(350, 500)
            time.sleep(0.2)
            led_G.off()
            time.sleep(0.1)
            list_User.append(3)
            i += 1
            erro = conferir_Jogada(i, pontos, erro)
            
        elif value_G == 1:
            led_B.on()
            play_tone(300, 500)
            time.sleep(0.2)
            led_B.off()
            time.sleep(0.1)
            list_User.append(4)
            i += 1
            erro = conferir_Jogada(i, pontos, erro)
            
        else:
            pass
        
        # Verifica o valor da variável erro para poder validar o game over
        if erro == 1:
            erro = 1
            data = {
                "Nome" : nome,
                "Pontos" : pontos,
            }
            erroJogador()
            enviarFire(data)
            break
        
    if erro != 1:
        pontos += 1
        proxNivel()
        print(f"Nível {pontos + 1}")
        time.sleep(1)
        
            
        