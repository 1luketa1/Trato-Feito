import json


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