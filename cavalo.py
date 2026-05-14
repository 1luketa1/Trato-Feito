from fastapi import APIRouter
from bson import ObjectId

from database import cavalos_collection

from services.NeoService import (
    CreateHorse,
    UpdateHorseName,
    DeleteHorse
)

router = APIRouter(prefix="/cavalos")


@router.get("/")
def listar_cavalos():

    cavalos = []

    for cavalo in cavalos_collection.find():

        cavalo["_id"] = str(cavalo["_id"])

        cavalos.append(cavalo)

    return cavalos


@router.get("/{id}")
def buscar_cavalo(id: str):


    cavalo = cavalos_collection.find_one({
        "_id": ObjectId(id)
    })

    if cavalo:
        cavalo["_id"] = str(cavalo["_id"])

    
    # =====================================
        # CRIA NO NEO4J
        # =====================================

        CreateHorse(
            dBAcessKey=cavalo["_id"],
            name=cavalo.get("nome", "Sem nome")
        )

    return cavalo


@router.post("/")
def criar_cavalo(cavalo: dict):

    resultado = cavalos_collection.insert_one(cavalo)

    cavalo_id = str(
        resultado.inserted_id
    )
    
    # cria no Neo4j
    CreateHorse(
        dBAcessKey=str(cavalo_id),
        name=cavalo.get("nome")
    )

    return {
        "id": cavalo_id
    }


@router.put("/{id}")
def atualizar_cavalo(id: str, cavalo: dict):

    cavalos_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": cavalo}
    )

    # atualiza no Neo4j
    UpdateHorseName(
        dBAcessKey=id,
        name=cavalo.get("nome")
    )

    return {
        "msg": "Cavalo atualizado"
    }


@router.delete("/{id}")
def deletar_cavalo(id: str):

    cavalos_collection.delete_one({
        "_id": ObjectId(id)
    })

    # deleta no Neo4j
    DeleteHorse(
        dBAcessKey=id
    )

    return {
        "msg": "Cavalo deletado"
    }