from fastapi import APIRouter
from bson import ObjectId

from database import pistas_collection

router = APIRouter(prefix="/pistas")


@router.get("/")
def listar_pistas():

    pistas = []

    for pista in pistas_collection.find():

        pista["_id"] = str(pista["_id"])

        pistas.append(pista)

    return pistas


@router.get("/{id}")
def buscar_pista(id: str):

    pista = pistas_collection.find_one({
        "_id": ObjectId(id)
    })

    if pista:
        pista["_id"] = str(pista["_id"])

    return pista


@router.post("/")
def criar_pista(pista: dict):

    resultado = pistas_collection.insert_one(pista)

    return {
        "id": str(resultado.inserted_id)
    }


@router.put("/{id}")
def atualizar_pista(id: str, pista: dict):

    pistas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": pista}
    )

    return {"msg": "Pista atualizada"}


@router.delete("/{id}")
def deletar_pista(id: str):

    pistas_collection.delete_one({
        "_id": ObjectId(id)
    })

    return {"msg": "Pista deletada"}