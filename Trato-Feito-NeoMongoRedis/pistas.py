from fastapi import APIRouter
from bson import ObjectId

from database import pistas_collection

# =========================================
# NEO4J
# =========================================

from services.NeoService import (
    CreateTrack,
    DeleteTrack
)

router = APIRouter(prefix="/pistas")


# =========================================
# LISTAR
# =========================================

@router.get("/")
def listar_pistas():

    pistas = []

    for pista in pistas_collection.find():

        pista["_id"] = str(pista["_id"])

        pistas.append(pista)

    return pistas


# =========================================
# BUSCAR
# =========================================

@router.get("/{id}")
def buscar_pista(id: str):

    pista = pistas_collection.find_one({
        "_id": ObjectId(id)
    })

    if pista:
        pista["_id"] = str(pista["_id"])

    return pista


# =========================================
# CRIAR
# =========================================

@router.post("/")
def criar_pista(pista: dict):

    resultado = pistas_collection.insert_one(
        pista
    )

    pista_id = str(
        resultado.inserted_id
    )

    # =====================================
    # NEO4J
    # =====================================

    CreateTrack(
        dBAcessKey=pista_id,
        name=pista.get("nome", "")
    )

    return {
        "id": pista_id
    }


# =========================================
# ATUALIZAR
# =========================================

@router.put("/{id}")
def atualizar_pista(
    id: str,
    pista: dict
):

    pistas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": pista}
    )

    # =====================================
    # OPCIONAL:
    # Se tiver UpdateTrack no NeoService
    # =====================================

    """
    UpdateTrack(
        dBAcessKey=id,
        name=pista.get("nome", "")
    )
    """

    return {
        "msg": "Pista atualizada"
    }


# =========================================
# DELETAR
# =========================================

@router.delete("/{id}")
def deletar_pista(id: str):

    pistas_collection.delete_one({
        "_id": ObjectId(id)
    })

    # =====================================
    # NEO4J
    # =====================================

    DeleteTrack(
        dBAcessKey=id
    )

    return {
        "msg": "Pista deletada"
    }