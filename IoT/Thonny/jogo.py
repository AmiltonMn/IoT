import machine
from machine import SoftI2C, Pin
import time



# Configuração dos pinos do LCD
#rs = Pin(13, Pin.OUT)
#e = Pin(12, Pin.OUT)
#d4 = Pin(14, Pin.OUT)
#d5 = Pin(27, Pin.OUT)
#d6 = Pin(26, Pin.OUT)
#d7 = Pin(25, Pin.OUT)
#button = Pin(35, Pin.IN)
button2 = Pin(35, Pin.IN)
#pir_sensor = Pin(34, Pin.IN)

rs = Pin(14, Pin.OUT)
e = Pin(13, Pin.OUT)
d4 = Pin(12, Pin.OUT)
d5 = Pin(27, Pin.OUT)
d6 = Pin(26, Pin.OUT)
d7 = Pin(25, Pin.OUT)
button = machine.Pin(34, machine.Pin.IN)

def read_pir_sensor():
    if pir_sensor.value() == 1:
        print("Movimento Perto")
    else:
        print("Nenhum movimento.")
        
def pulse_enable():
    e.on()
    time.sleep_us(1)
    e.off()
    time.sleep_us(50)

def send_nibble(data):
    d4.value((data >> 0) & 1)
    d5.value((data >> 1) & 1)
    d6.value((data >> 2) & 1)
    d7.value((data >> 3) & 1)
    pulse_enable()

def send_byte(data, rs_value):
    rs.value(rs_value)
    send_nibble(data >> 4)  # Envia o nibble superior
    send_nibble(data & 0x0F)  # Envia o nibble inferior

def lcd_command(cmd):
    send_byte(cmd, 0)

def lcd_data(data):
    send_byte(data, 1)
    
def create_char(location, charmap):
    location &= 0x7
    send_byte(0x40 | (location << 3), False)
    for i in range(8):
        send_byte(charmap[i], True)

def lcd_init():
    time.sleep(0.05)
    rs.off()
    e.off()
    send_nibble(0x03)
    time.sleep_ms(5)
    send_nibble(0x03)
    time.sleep_us(150)
    send_nibble(0x03)
    send_nibble(0x02)
    lcd_command(0x28)  # Função set: 4 bits, 2 linhas, 5x8 pontos
    lcd_command(0x0C)  # Display on, cursor off, blink off
    lcd_command(0x06)  # Entry mode set: incrementa e sem shift
    lcd_command(0x01)  # Limpa o display
    time.sleep_ms(2)
    
def lcd_clear():
    lcd_command(0x01)  # Limpa o display
    time.sleep_ms(2)

def lcd_puts(text):
    for char in text:
        lcd_data(ord(char))
        
def lcd_goto(linha, coluna):
    
    # Check if line or column is out of bounds
    if (linha < 0 or linha > 1) or (coluna < 0):
        print("Invalid line or column. Ignoring goto command.")
        return

    # Adjust column for different line widths (15 chars for line 0, 16 chars for line 1)
    if linha == 0:
        max_coluna = 14  # 15 characters on line 0
    else:
        max_coluna = 15  # 16 characters on line 1

    # Ensure column doesn't exceed maximum
    if coluna > max_coluna:
        coluna = max_coluna

    # Calculate DDRAM address
    address = (linha * 0x40) + coluna  # The address calculation is different for the second line
    lcd_command(0x80 | address)  # Send DDRAM address set command with address

# Inicio do código do jogo

lcd_init()
cont = 0

pessoa = [
  0b01110,
  0b01010,
  0b01110,
  0b00100,
  0b11111,
  0b00100,
  0b01010,
  0b10001,
]

jumper = [
  0b01110,
  0b01010,
  0b01110,
  0b00101,
  0b01110,
  0b10100,
  0b01011,
  0b11001
  ]

missile = [
  0b00000,
  0b00001,
  0b00001,
  0b00110,
  0b11100,
  0b00110,
  0b00001,
  0b00001,
]

posPessoa = 0
morte = "<"                                                                                                                                                                                                                           
posM = 16
pontos = 0
inicio = 0
ligado = button.value()

while True:
    create_char(0, pessoa)
    create_char(1, jumper)
    create_char(2, missile)
    ligadoIn = button2.value()
    time.sleep(0.1)
    lcd_goto(0, 5)
    lcd_puts("START!")
    if ligadoIn == 1:
        break
    else:
        continue
        

while True:
        ligadoButton = button.value()
        #ligado = pir_sensor()
        lcd_goto(1, 0)
        send_byte(0x00, pessoa)
        time.sleep(0.3)
        
        if ligado == 1 or ligadoButton == 1:
            lcd_clear()
            lcd_goto(0, 0)
            send_byte(0x01, jumper)
            time.sleep(0.3)
            lcd_clear()
            lcd_goto(1, posM)
            send_byte(0x02, missile)
            time.sleep(0.3)
            posM -= 1
            lcd_clear()
            
        lcd_goto(1, posM)
        send_byte(0x02, missile)
        time.sleep(0.1)
        posM -= 1
        lcd_clear()
        
        if posM < 0:
            posM = 16
            pontos += 1
            
        if posPessoa == posM:
            lcd_goto(0, 6)
            lcd_puts("GAME")
            lcd_goto(1, 6)
            lcd_puts("OVER")
            pontos = 0
            while True:
                ligadoIn = button2.value()
                time.sleep(0.1)
                if ligadoIn == 1:
                    posM = 16
                    pontos = 0
                    break;
                else:
                    continue   
        
        lcd_goto(0, 15)
        lcd_puts(f"{pontos}")

    
        
        
        
        






        

