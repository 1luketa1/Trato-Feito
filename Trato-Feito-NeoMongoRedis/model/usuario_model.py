import json
from datetime import datetime
import os

class Usuario:

    @staticmethod
    def carregar_config():

        try:

            with open("config.json", "r", encoding="utf-8") as arquivo:

                return json.load(arquivo)

        except:

            return {
                "tema": "Claro",
                "idioma": "Português",
                "nivel_aposta": "Normal"
            }

    @staticmethod
    def salvar_config(tema, idioma, nivel_aposta):

        config = {
            "tema": tema,
            "idioma": idioma,
            "nivel_aposta": nivel_aposta
        }

        with open("config.json", "w", encoding="utf-8") as arquivo:

            json.dump(
                config,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def autenticar(usuario, senha):

        if usuario == "admin" and senha == "123":

            config = Usuario.carregar_config()

            return {
                "usuario": usuario,
                "saldo": 1500.75,
                "tema": config["tema"],
                "idioma": config["idioma"],
                "nivel_aposta": config["nivel_aposta"]
            }

        return None
    
    @staticmethod
    def salvar_pesquisa(usuario, texto):

        arquivo = "pesquisas.json"

        pesquisas = {}

        if os.path.exists(arquivo):

            with open(arquivo, "r", encoding="utf-8") as f:

                pesquisas = json.load(f)

        if usuario not in pesquisas:

            pesquisas[usuario] = []

        pesquisas[usuario].append({
            "pesquisa": texto,
            "horario": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

        pesquisas[usuario] = pesquisas[usuario][-15:]

        with open(arquivo, "w", encoding="utf-8") as f:

            json.dump(
                pesquisas,
                f,
                indent=4,
                ensure_ascii=False
            )