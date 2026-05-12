import requests

API_URL = "http://127.0.0.1:8000"


def listar_corridas():

    response = requests.get(f"{API_URL}/corridas/")

    return response.json()


def buscar_corrida(corrida_id):

    response = requests.get(
        f"{API_URL}/corridas/{corrida_id}"
    )

    return response.json()

def listar_corridas_ativas():

    response = requests.get(
        f"{API_URL}/corridas/ativas"
    )

    return response.json()


def listar_corridas_finalizadas():

    response = requests.get(
        f"{API_URL}/corridas/finalizadas"
    )

    return response.json()