import pyodbc
import time
import requests
import json

proxies = {'https':"http://disrct:etsps2024401@10.224.200.26:8080"}
FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/Amilton.json"
server = 'CA-C-0065C\SQLEXPRESS'
database = 'Amilton'
cnxn = pyodbc.connect('DRIVER={SQL server}; SERVER=' + server +';DATABASE=' + database + ';Trusted_Connection=yes')
cursor = cnxn.cursor()


def InserirBD(sinal):
    server = 'CA-C-0065C\SQLEXPRESS'
    database = 'Amilton'
    cursor.execute(f"INSERT Genius (Pontos, Nome) VALUES ({sinal['Pontos']}, '{sinal['Nome']}')")
    cursor.commit()
    print("Inserido com sucesso!")

def pegarTabela():
    cursor.execute(f"Select * from dbo.Genius")
    tabela = cursor.fetchall()
    return tabela 
    

def pegarMaior():
    cursor.execute(f"Select * from Genius order by Pontos DESC")

    tabela = cursor.fetchall()
    return tabela

def apresentar(sinal):
    print(f"Pontos: {sinal['Pontos']}")

recordes = [[],[]]

# sinal = json.loads(requests.get(FIREBASE_URL, proxies=proxies).content)
# InserirBD(sinal)
tabela = pegarMaior()
for row in tabela:
    recordes[0].append(row[1])
    recordes[1].append(row[2])

while True:
    sinal = json.loads(requests.get(FIREBASE_URL, proxies=proxies).content)

    comp = sinal['Pontos']

    print(comp)

    if comp > recordes[0][0]:
        InserirBD(sinal)
        tabela = pegarMaior()
        recordes[1][0] = sinal['Nome']
        recordes[0][0] = comp

    for row in tabela:
        recordes[0].append(row[1])
        recordes[1].append(row[2])

    print(f"Recorde atual: {recordes[1][0]} com {recordes[0][0]} pontos!")
    time.sleep(5)