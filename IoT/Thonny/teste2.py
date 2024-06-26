from machine import Pin, SPI
import time

# Configura os pinos SPI e controle do display
spi = SPI(1, baudrate=40000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
cs = Pin(5, Pin.OUT)
dc = Pin(16, Pin.OUT)
rst = Pin(17, Pin.OUT)

# Função para enviar comandos ao display
def lcd_command(cmd):
    dc.value(0)  # Comando
    cs.value(0)
    spi.write(bytearray([cmd]))
    cs.value(1)

# Função para enviar dados ao display
def lcd_data(data):
    dc.value(1)  # Dados
    cs.value(0)
    spi.write(bytearray([data]))
    cs.value(1)

# Inicializa o display
def lcd_init():
    rst.value(0)
    time.sleep_ms(50)
    rst.value(1)
    time.sleep_ms(50)

    lcd_command(0x01)  # Software reset
    time.sleep_ms(150)

    lcd_command(0x28)  # Display OFF

    lcd_command(0xCF)
    lcd_data(0x00)
    lcd_data(0xC1)
    lcd_data(0x30)

    lcd_command(0xED)
    lcd_data(0x64)
    lcd_data(0x03)
    lcd_data(0x12)
    lcd_data(0x81)

    lcd_command(0xE8)
    lcd_data(0x85)
    lcd_data(0x00)
    lcd_data(0x78)

    lcd_command(0xCB)
    lcd_data(0x39)
    lcd_data(0x2C)
    lcd_data(0x00)
    lcd_data(0x34)
    lcd_data(0x02)

    lcd_command(0xF7)
    lcd_data(0x20)

    lcd_command(0xEA)
    lcd_data(0x00)
    lcd_data(0x00)

    lcd_command(0xC0)    # Power control
    lcd_data(0x23)       # VRH[5:0]

    lcd_command(0xC1)    # Power control
    lcd_data(0x10)       # SAP[2:0];BT[3:0]

    lcd_command(0xC5)    # VCM control
    lcd_data(0x3e)       # Contrast
    lcd_data(0x28)

    lcd_command(0xC7)    # VCM control2
    lcd_data(0x86)       # --

    lcd_command(0x36)    # Memory Access Control
    lcd_data(0x48)

    lcd_command(0x3A)
    lcd_data(0x55)

    lcd_command(0xB1)
    lcd_data(0x00)
    lcd_data(0x18)

    lcd_command(0xB6)    # Display Function Control
    lcd_data(0x08)
    lcd_data(0x82)
    lcd_data(0x27)

    lcd_command(0xF2)    # 3Gamma Function Disable
    lcd_data(0x00)

    lcd_command(0x26)    # Gamma curve selected
    lcd_data(0x01)

    lcd_command(0xE0)    # Set Gamma
    lcd_data(0x0F)
    lcd_data(0x31)
    lcd_data(0x2B)
    lcd_data(0x0C)
    lcd_data(0x0E)
    lcd_data(0x08)
    lcd_data(0x4E)
    lcd_data(0xF1)
    lcd_data(0x37)
    lcd_data(0x07)
    lcd_data(0x10)
    lcd_data(0x03)
    lcd_data(0x0E)
    lcd_data(0x09)
    lcd_data(0x00)

    lcd_command(0xE1)    # Set Gamma
    lcd_data(0x00)
    lcd_data(0x0E)
    lcd_data(0x14)
    lcd_data(0x03)
    lcd_data(0x11)
    lcd_data(0x07)
    lcd_data(0x31)
    lcd_data(0xC1)
    lcd_data(0x48)
    lcd_data(0x08)
    lcd_data(0x0F)
    lcd_data(0x0C)
    lcd_data(0x31)
    lcd_data(0x36)
    lcd_data(0x0F)

    lcd_command(0x11)    # Exit Sleep
    time.sleep_ms(120)
    lcd_command(0x29)    # Display on
    lcd_command(0x2C)    # Memory Write

# Função para preencher o display com uma cor
def lcd_fill(color):
    lcd_command(0x2A)  # Coluna
    lcd_data(0x00)
    lcd_data(0x00)
    lcd_data(0x00)
    lcd_data(0xEF)

    lcd_command(0x2B)  # Linha
    lcd_data(0x00)
    lcd_data(0x00)
    lcd_data(0x01)
    lcd_data(0x3F)

    lcd_command(0x2C)  # Escreve na memória

    for _ in range(240 * 320):
        lcd_data(color >> 8)
        lcd_data(color & 0xFF)

# Inicializa e preenche o display com preto
lcd_init()
black = 0x0000
lcd_fill(black)