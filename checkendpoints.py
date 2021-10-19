import requests
import json
import datetime

BASE_URL = 'http://localhost:8082'
# Create Personal [POST]
def create_personal(base_url: str):
    personal = {
        "legajo": "1232335",
        "nombre": "pepe",
        "apellido": "popo",
        "sector": "oscuro",
        "categoria": 8,
        "password": "1234",
        "fechaIngreso": datetime.datetime.now(),
    }
    request = requests.post(f"{base_url}/personal", data=personal)

    return request.text

def main():
    response = create_personal(BASE_URL)

    print(response)


if __name__ == "__main__":
    main()