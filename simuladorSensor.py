import requests
import random
import time

url = 'http://127.0.0.1:5000/datos_sensor'

while True:
    temperatura = round(random.uniform(20,30),2)
    humedad = round(random.uniform(40,60),2)
    
    payload = {
        'temperatura':temperatura,
        'humedad':humedad,
        'timestamp':time.time()
    }
    
    response = requests.post(url,json=payload)
    print(response,payload)
    
    time.sleep(5)

