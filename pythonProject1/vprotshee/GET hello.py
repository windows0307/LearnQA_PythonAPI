import requests


payload = {"name":"Users"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response.text)