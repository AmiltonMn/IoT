import requests
import json

proxies = {'https':"http://disrct:etsps2024401@10.224.200.26:8080"}

nome = input("Digite seu nome: ")

url = f'https://api.agify.io?name={nome}'
data = json.loads(requests.get(url, proxies=proxies).content)['age']

print(f"Sua idade estimada no mundo é de {data} anos!")