from fastapi import APIRouter
from bson import ObjectId

from database import cavalos_collection

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

    return cavalo


@router.post("/")
def criar_cavalo(cavalo: dict):

    resultado = cavalos_collection.insert_one(cavalo)

    return {
        "id": str(resultado.inserted_id)
    }


@router.put("/{id}")
def atualizar_cavalo(id: str, cavalo: dict):

    cavalos_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": cavalo}
    )

    return {"msg": "Cavalo atualizado"}


@router.delete("/{id}")
def deletar_cavalo(id: str):

    cavalos_collection.delete_one({
        "_id": ObjectId(id)
    })

    return {"msg": "Cavalo deletado"}