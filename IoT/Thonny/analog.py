from machine import ADC, Pin, SoftI2C
import time
import dht

rs = Pin(14, Pin.OUT)
e = Pin(13, Pin.OUT)
d4 = Pin(12, Pin.OUT)
d5 = Pin(26, Pin.OUT)
d6 = Pin(27, Pin.OUT)
d7 = Pin(25, Pin.OUT)
luz = Pin(5, Pin.IN)

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

def lcd_goto(linha, coluna):
    
    # Verifica se a linha ou a coluna estão fora do alcance
    if (linha < 0 or linha > 1) or (coluna < 0):
        print("Invalid line or column. Ignoring goto command.")
        return

    # Austa coluna para diferentes tamanhos de linha (15 chars para linha 0, 16 chars para linha 1)
    if linha == 0:
        max_coluna = 14  # 15 characters na linha 0
    else:
        max_coluna = 15  # 16 characters na linha 1

    # Certifica que não vai passar do máximo de colunas
    if coluna > max_coluna:
        coluna = max_coluna

    # Calcula endereço DDRAM
    address = (linha * 0x40) + coluna  # O cálculo de endereço é diferente para a segunda linha
    lcd_command(0x80 | address)  # Manda o endereço DDRAM seta comando com o endereço

# Configura o pino ADC onde o potenciômetro está conectado

adc = ADC(Pin(34))
adc.width(ADC.WIDTH_12BIT) # Configura a resolução do ADC
adc.atten(ADC.ATTN_11DB) # Configura a atenuação

def create_char(location, charmap):
    location &= 0x7
    send_byte(0x40 | (location << 3), False)
    for i in range(8):
        send_byte(charmap[i], True)

# Função de leitrua do potenciômetro
def read_potentiometer():
    # Lê o valor do ADC (Potenciômetro)
    pot_value = (adc.read()*15/4095)
    print(f"Valor do potenciômetro:", round(pot_value))
    time.sleep(1)
    
lcd_init()

pessoa = [
  0b01110,
  0b01010,
  0b01110,
  0b00100,
  0b11111,
  0b00100,
  0b01010,
  0b01010,
]

pessoa2 = [
  0b01110,
  0b01010,
  0b01110,
  0b00101,
  0b11111,
  0b10100,
  0b01011,
  0b11001,
]

create_char(1, pessoa)
create_char(2, pessoa2)

while True:
    luz_valor = luz.value()
    
    # Lê potenciometro
    pot_value = round((adc.read()*15/4095))
    time.sleep(0.1)
    
    if luz_valor == 0:
        print(f"Número Par: {luz_valor}")
        lcd_goto(0, pot_value)
        send_byte(0x01, pessoa)
        time.sleep(0.5)
    else:
        print(f"Número Ímpar: {luz_valor}")
        lcd_goto(0, pot_value)
        send_byte(0x02, pessoa2)
        time.sleep(0.5)
        
    lcd_clear()