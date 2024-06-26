import pyodbc
import time
import requests
import json
import matplot

server = 'CA-C-0065C\SQLEXPRESS'
database = 'Amilton'
cnxn = pyodbc.connect('DRIVER={SQL server}; SERVER=' + server +';DATABASE=' + database + ';Trusted_Connection=yes')
cursor = cnxn.cursor()
proxies = {'https':"http://disrct:etsps2024401@10.224.200.26:8080"}

FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/Amilton.json"

def InserirBD(sinal):
    cursor.execute(f"INSERT Sensor (Temperatura, Umidade) VALUES ({sinal['Temperatura:']}, {sinal['Umidade:']})")
    cursor.commit()
    print("Inserido com sucesso!")

def pegarTabela():
    cursor.execute(f"Select * from Sensor")

def apresentar(sinal):
    print(f"Temperatura: {sinal['Temperatura:']}")
    print(f"Umidade: {sinal['Umidade:']}")

while True:
    data = json.loads(requests.get(FIREBASE_URL, proxies=proxies).content)
    print(data)
    valores = (data)
    apresentar(valores)
    InserirBD(valores)
    time.sleep(120)
    time.sleep(1)

