from fastapi import APIRouter
from bson import ObjectId

from database import corridas_collection

router = APIRouter(prefix="/corridas")


@router.get("/")
def listar_corridas():

    corridas = []

    for corrida in corridas_collection.find():

        corrida["_id"] = str(corrida["_id"])

        corrida["pista_id"] = str(corrida["pista_id"])

        corrida["cavalos"] = [
            str(c) for c in corrida["cavalos"]
        ]

        if "resultado" in corrida:

            for item in corrida["resultado"]:

                item["cavalo_id"] = str(item["cavalo_id"])

        corridas.append(corrida)

    return corridas


@router.get("/{id}")
def buscar_corrida(id: str):

    corrida = corridas_collection.find_one({
        "_id": ObjectId(id)
    })

    if corrida:

        corrida["_id"] = str(corrida["_id"])

        corrida["pista_id"] = str(corrida["pista_id"])

        corrida["cavalos"] = [
            str(c) for c in corrida["cavalos"]
        ]

        if "resultado" in corrida:

            for item in corrida["resultado"]:

                item["cavalo_id"] = str(item["cavalo_id"])

    return corrida


@router.post("/")
def criar_corrida(corrida: dict):

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
        "id": str(resultado.inserted_id)
    }


@router.put("/{id}")
def atualizar_corrida(id: str, corrida: dict):

    if "pista_id" in corrida:

        corrida["pista_id"] = ObjectId(
            corrida["pista_id"]
        )

    if "cavalos" in corrida:

        corrida["cavalos"] = [
            ObjectId(c)
            for c in corrida["cavalos"]
        ]

    if "resultado" in corrida:

        for item in corrida["resultado"]:

            item["cavalo_id"] = ObjectId(
                item["cavalo_id"]
            )

    corridas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": corrida}
    )

    return {"msg": "Corrida atualizada"}


@router.delete("/{id}")
def deletar_corrida(id: str):

    corridas_collection.delete_one({
        "_id": ObjectId(id)
    })

    return {"msg": "Corrida deletada"}