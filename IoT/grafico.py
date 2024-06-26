import pyodbc
import time
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

server = 'CA-C-0065C\\SQLEXPRESS'
database = 'Amilton'
cnxn = pyodbc.connect('DRIVER={SQL server}; SERVER=' + server +';DATABASE=' + database + ';Trusted_Connection=yes')
cursor = cnxn.cursor()
proxies = {'https':"http://disrct:etsps2024401@10.224.200.26:8080"}

FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/Amilton.json"

def pegarTabela():
    cursor.execute(f"Select * from Sensor")
    data = cursor.fetchall()
    print("Leitura de SQL concluída!")
    return data

i = 0
val = [[], [], [], []]

while True:
    data = (pegarTabela())
    for row in data:
        val[0].append(row[0])
        val[1].append(row[1])
        val[2].append(row[2])
        val[3].append(row[3])

    # Criando o gráfico
    plt.figure(figsize=(10, 8), layout='constrained') # Define o tamanho e o layout do gráfico

    # Define as linhas que estarão no gráfico
    plt.plot(val[3], val[1], label = 'Temperatura', color='red', marker='o') 
    plt.plot(val[3], val[2], label = 'Umidade', color='blue', marker='o')

    # Definição de Eixos
    plt.axis((val[3][0], val[3][len(val[3]) - 1], 0, 50))

    plt.grid(linestyle='dashed', c='grey')
    plt.title('Gráfico 1')
    plt.legend()
    plt.show()

    plt.style.use('_mpl-gallery')

    # Prepare some coordinates
    x, y, z = np.indices((8, 8, 8))

    # Draw cuboids in the top left and bottom right corners
    cube1 = (x < 3) & (y < 3) & (z < 3)
    cube2 = (x >= 5) & (y >= 5) & (z >= 5)

    # Combine the objects into a single boolean array
    voxelarray = cube1 | cube2

    # Plot
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.voxels(voxelarray, edgecolor='k')

    ax.set(xticklabels=[],
        yticklabels=[],
        zticklabels=[])

    plt.show()