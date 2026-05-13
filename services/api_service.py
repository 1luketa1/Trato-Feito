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



def listar_pistas():

    response = requests.get(
        f"{API_URL}/pistas/"
    )

    return response.json()


def listar_cavalos():

    response = requests.get(
        f"{API_URL}/cavalos/"
    )

    return response.json()


def criar_corrida(dados):

    response = requests.post(
        f"{API_URL}/corridas/",
        json=dados
    )

    return response.json()

def simular_corrida(id):

    response = requests.post(
        f"{API_URL}/corridas/{id}/simular"
    )

    return response.json()