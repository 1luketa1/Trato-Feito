from database import (
    corridas_collection,
    cavalos_collection,
    pistas_collection
)

from bson import ObjectId


class CorridaModel:

    @staticmethod
    def listar_corridas():

        corridas = []

        for corrida in corridas_collection.find():

            corrida["_id"] = str(corrida["_id"])
            corrida["pista_id"] = str(corrida["pista_id"])

            corridas.append(corrida)

        return corridas

    @staticmethod
    def buscar_corrida(id_corrida):

        corrida = corridas_collection.find_one({
            "_id": ObjectId(id_corrida)
        })

        if not corrida:
            return None

        corrida["_id"] = str(corrida["_id"])


        pista = pistas_collection.find_one({
            "_id": corrida["pista_id"]
        })

        if pista:

            pista["_id"] = str(pista["_id"])


        cavalos = []

        for cavalo_id in corrida["cavalos"]:

            cavalo = cavalos_collection.find_one({
                "_id": cavalo_id
            })

            if cavalo:

                cavalo["_id"] = str(cavalo["_id"])

                cavalos.append(cavalo)

        corrida["pista"] = pista
        corrida["cavalos_info"] = cavalos

        return corrida