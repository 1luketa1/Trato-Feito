import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

ARQUIVO = "usuarios.json"


class RedisService:

    # ===============================
    # CRIAR USUÁRIO
    # ===============================
    @staticmethod
    def criar_usuario(nome, senha):

        # verifica duplicação
        for chave in r.keys("usuario:*"):
            usuario = r.hgetall(chave)

            if usuario.get("nome", "").lower() == nome.lower():
                return False

        # gera ID
        usuarioId = r.incr("proximoUsuarioId")

        # salva no Redis
        r.hset(f"usuario:{usuarioId}", mapping={
            "id": usuarioId,
            "nome": nome,
            "senha": senha,
            "saldo": 0
        })

        # salva no JSON
        RedisService.salvar_json()

        return True

    # ===============================
    # LOGIN
    # ===============================
    @staticmethod
    def autenticar(nome, senha):

        for chave in r.keys("usuario:*"):

            usuario = r.hgetall(chave)

            if (
                usuario.get("nome") == nome and
                usuario.get("senha") == senha
            ):
                return {
                    "id": usuario["id"],
                    "usuario": usuario["nome"],
                    "saldo": float(usuario["saldo"])
                }

        return None

    # ===============================
    # ATUALIZAR SALDO
    # ===============================
    @staticmethod
    def atualizar_saldo(usuario_id, saldo):

        chave = f"usuario:{usuario_id}"

        if not r.exists(chave):
            return

        r.hset(chave, "saldo", saldo)

        # salva no JSON
        RedisService.salvar_json()

    # ===============================
    # SALVAR JSON (AUTOMÁTICO)
    # ===============================
    @staticmethod
    def salvar_json():

        usuarios = []

        for chave in r.keys("usuario:*"):
            usuarios.append(r.hgetall(chave))

        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(
                usuarios,
                f,
                indent=4,
                ensure_ascii=False
            )

    # ===============================
    # CARREGAR JSON → REDIS
    # ===============================
    @staticmethod
    def carregar_json():

        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

                # limpa redis antes
                r.flushdb()

                for usuario in usuarios:

                    usuario_id = usuario["id"]

                    r.hset(
                        f"usuario:{usuario_id}",
                        mapping=usuario
                    )

                # ajusta contador
                if usuarios:
                    ultimo_id = max(
                        int(u["id"]) for u in usuarios
                    )
                    r.set("proximoUsuarioId", ultimo_id)

        except FileNotFoundError:
            pass