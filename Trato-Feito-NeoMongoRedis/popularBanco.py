from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
from datetime import datetime

# =========================================
# NEO4J
# =========================================
from services.NeoService import (
    CreateHorse,
    CreateTrack,
    CreateRun
)

# carregar .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["Aposta"]

# coleções
cavalos_collection = db["Cavalos"]
pistas_collection = db["Pistas"]
corridas_collection = db["Corridas"]

# =========================================
# LIMPAR
# =========================================

cavalos_collection.delete_many({})
pistas_collection.delete_many({})
corridas_collection.delete_many({})

print("Coleções limpas.")

# =========================================
# FUNÇÕES (IGUAIS À API)
# =========================================

def criar_cavalo(cavalo: dict):
    resultado = cavalos_collection.insert_one(cavalo)
    cavalo_id = str(resultado.inserted_id)

    CreateHorse(
        dBAcessKey=cavalo_id,
        name=cavalo.get("nome", "")
    )

    return cavalo_id


def criar_pista(pista: dict):
    resultado = pistas_collection.insert_one(pista)
    pista_id = str(resultado.inserted_id)

    CreateTrack(
        dBAcessKey=pista_id,
        name=pista.get("nome", "")
    )

    return pista_id


def criar_corrida(corrida: dict):
    pista_id_original = corrida["pista_id"]
    cavalos_originais = corrida["cavalos"]

    corrida_mongo = corrida.copy()

    corrida_mongo["pista_id"] = ObjectId(pista_id_original)
    corrida_mongo["cavalos"] = [
        ObjectId(c) for c in cavalos_originais
    ]

    resultado = corridas_collection.insert_one(corrida_mongo)
    corrida_id = str(resultado.inserted_id)

    CreateRun(
        date=corrida["data"].isoformat(),
        horsesDBAcessKeys=cavalos_originais,
        trackDBAcessKey=pista_id_original,
        dBAcessKey=corrida_id
    )

    return corrida_id


# =========================================
# INSERIR CAVALOS (COMPLETO)
# =========================================

cavalos = [
    {
        "nome": "Trovão Negro",
        "idade": 5,
        "estatisticas": {
            "velocidade_maxima": 78,
            "velocidade_media": 65,
            "aceleracao": 8.7,
            "resistencia": 8.1,
            "consistencia": 0.91
        },
        "estado": {
            "fadiga": 0.10,
            "dias_desde_ultima_corrida": 7
        },
        "perfil": {
            "distancia_preferida": 5,
            "tipo_pista_preferida": "seca"
        }
    },
    {
        "nome": "Furacão Azul",
        "idade": 4,
        "estatisticas": {
            "velocidade_maxima": 82,
            "velocidade_media": 68,
            "aceleracao": 9.1,
            "resistencia": 7.3,
            "consistencia": 0.88
        },
        "estado": {
            "fadiga": 0.20,
            "dias_desde_ultima_corrida": 5
        },
        "perfil": {
            "distancia_preferida": 4,
            "tipo_pista_preferida": "seca"
        }
    },
    {
        "nome": "Tempestade Real",
        "idade": 6,
        "estatisticas": {
            "velocidade_maxima": 74,
            "velocidade_media": 63,
            "aceleracao": 7.4,
            "resistencia": 9.0,
            "consistencia": 0.95
        },
        "estado": {
            "fadiga": 0.05,
            "dias_desde_ultima_corrida": 12
        },
        "perfil": {
            "distancia_preferida": 7,
            "tipo_pista_preferida": "lama"
        }
    },
    {
        "nome": "Relâmpago Branco",
        "idade": 3,
        "estatisticas": {
            "velocidade_maxima": 85,
            "velocidade_media": 70,
            "aceleracao": 9.5,
            "resistencia": 6.9,
            "consistencia": 0.80
        },
        "estado": {
            "fadiga": 0.30,
            "dias_desde_ultima_corrida": 3
        },
        "perfil": {
            "distancia_preferida": 3,
            "tipo_pista_preferida": "seca"
        }
    },
    {
        "nome": "Guardião da Serra",
        "idade": 7,
        "estatisticas": {
            "velocidade_maxima": 70,
            "velocidade_media": 61,
            "aceleracao": 6.8,
            "resistencia": 9.4,
            "consistencia": 0.97
        },
        "estado": {
            "fadiga": 0.08,
            "dias_desde_ultima_corrida": 15
        },
        "perfil": {
            "distancia_preferida": 8,
            "tipo_pista_preferida": "lama"
        }
    }
]

cavalos_ids = [criar_cavalo(c) for c in cavalos]

print("Cavalos OK (completos + Neo4j)")

# =========================================
# INSERIR PISTAS
# =========================================

pistas = [
    {"nome": "Autódromo Central", "tipo": "seca", "distancia": 5},
    {"nome": "Vale da Lama", "tipo": "lama", "distancia": 7},
    {"nome": "Sprint Arena", "tipo": "seca", "distancia": 3}
]

pistas_ids = [criar_pista(p) for p in pistas]

print("Pistas OK")

# =========================================
# INSERIR CORRIDAS
# =========================================

corridas = [
    {
        "nome": "Grande Premio SP",
        "data": datetime(2026, 5, 10),
        "pista_id": pistas_ids[0],
        "cavalos": [cavalos_ids[0], cavalos_ids[1], cavalos_ids[3]]
    },
    {
        "nome": "Copa da Serra",
        "data": datetime(2026, 5, 18),
        "pista_id": pistas_ids[1],
        "cavalos": [cavalos_ids[2], cavalos_ids[4], cavalos_ids[0]]
    },
    {
        "nome": "Corrida Noturna",
        "data": datetime(2026, 5, 22),
        "pista_id": pistas_ids[2],
        "cavalos": [cavalos_ids[1], cavalos_ids[3], cavalos_ids[0]]
    }
]

for corrida in corridas:
    criar_corrida(corrida)

print("Corridas OK")

print("🔥 Banco 100% consistente (Mongo + Neo4j)")