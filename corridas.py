from fastapi import APIRouter
from bson import ObjectId
from datetime import datetime

from database import (
    corridas_collection,
    pistas_collection,
    cavalos_collection
)

router = APIRouter(prefix="/corridas")

def converter_objectid(obj):

    if isinstance(obj, list):

        return [
            converter_objectid(item)
            for item in obj
        ]

    if isinstance(obj, dict):

        novo = {}

        for chave, valor in obj.items():

            if isinstance(valor, ObjectId):

                novo[chave] = str(valor)

            else:

                novo[chave] = converter_objectid(valor)

        return novo

    return obj

@router.get("/")
def listar_corridas():

    corridas = []

    for corrida in corridas_collection.find():

        pista = pistas_collection.find_one({
            "_id": corrida["pista_id"]
        })

        if pista:

            corrida["pista"] = pista

        cavalos_formatados = []

        for cavalo_id in corrida["cavalos"]:

            cavalo = cavalos_collection.find_one({
                "_id": cavalo_id
            })

            if cavalo:

                cavalos_formatados.append(cavalo)

        corrida["cavalos"] = cavalos_formatados

        corridas.append(
            converter_objectid(corrida)
        )

    return corridas


@router.get("/ativas")
def listar_corridas_ativas():

    corridas = []

    for corrida in corridas_collection.find({
        "status": "ativa"
    }):

        corrida["_id"] = str(corrida["_id"])

        # ==========================================
        # PISTA
        # ==========================================

        pista = pistas_collection.find_one({
            "_id": corrida["pista_id"]
        })

        if pista:

            pista["_id"] = str(pista["_id"])

            corrida["pista"] = pista

            corrida["pista_id"] = str(
                corrida["pista_id"]
            )

        cavalos_formatados = []

        for cavalo_id in corrida["cavalos"]:

            cavalo = cavalos_collection.find_one({
                "_id": cavalo_id
            })

            if cavalo:

                cavalo["_id"] = str(cavalo["_id"])

                cavalos_formatados.append(cavalo)

        corrida["cavalos"] = cavalos_formatados

        if "resultado" in corrida:

            resultados_formatados = []

            for resultado in corrida["resultado"]:

                resultado["cavalo_id"] = str(
                    resultado["cavalo_id"]
                )

                resultados_formatados.append(
                    resultado
                )

            corrida["resultado"] = resultados_formatados

        corridas.append(corrida)

    return corridas


@router.get("/finalizadas")
def listar_corridas_finalizadas():

    corridas = []

    for corrida in corridas_collection.find({
        "status": "finalizada"
    }):

        corrida["_id"] = str(corrida["_id"])

        corridas.append(corrida)

    return corridas


@router.get("/{id}")
def buscar_corrida(id: str):

    corrida = corridas_collection.find_one({
        "_id": ObjectId(id)
    })

    if not corrida:

        return {
            "erro": "Corrida não encontrada"
        }

    pista = pistas_collection.find_one({
        "_id": corrida["pista_id"]
    })

    if pista:

        corrida["pista"] = pista

    cavalos_formatados = []

    for cavalo_id in corrida["cavalos"]:

        cavalo = cavalos_collection.find_one({
            "_id": cavalo_id
        })

        if cavalo:

            cavalos_formatados.append(cavalo)

    corrida["cavalos"] = cavalos_formatados

    return converter_objectid(corrida)

@router.post("/")
def criar_corrida(corrida: dict):

    try:
        corrida["data"] = datetime.strptime(
            corrida["data"],
            "%d-%m-%Y"
        )
    except:
        return {"erro": "Data inválida. Use DD-MM-AAAA"}

    corrida["pista_id"] = ObjectId(
        corrida["pista_id"]
    )

    corrida["cavalos"] = [
        ObjectId(c)
        for c in corrida["cavalos"]
    ]

    resultado = corridas_collection.insert_one(
        corrida
    )

    return {
        "msg": "Corrida criada",
        "id": str(resultado.inserted_id)
    }
    
    
@router.post("/{id}/simular")
def simular_corrida_api(id: str):

    from services.simulacao_service import simular_corrida

    resultado = simular_corrida(id)

    if not resultado:
        return {"erro": "Erro na simulação"}

    corridas_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "resultado": resultado["resultado"],
                "status": "finalizada"
            }
        }
    )

    return resultado