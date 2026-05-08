class Usuario:

    @staticmethod
    def autenticar(usuario, senha):

        if usuario == "admin" and senha == "123":

            return {
                "usuario": usuario,
                "saldo": 1500.0,
                "tema": "Claro",
                "idioma": "Português",
                "nivel_aposta": "Normal"
            }

        return None