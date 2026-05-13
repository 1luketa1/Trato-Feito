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


        # =====================================================
    # CRIAR TICKET
    # =====================================================

    @staticmethod
    def criar_ticket(
        nome_corrida,
        nome_cavalo,
        valor_pago,
        odd
    ):

        ticket_id = r.incr(
            "proximoTicketId"
        )

        r.hset(
            f"ticket:{ticket_id}",
            mapping={
                "id": ticket_id,
                "nome_corrida": nome_corrida,
                "nome_cavalo": nome_cavalo,
                "valor_pago": valor_pago,
                "odd": odd
            }
        )

        RedisService.salvar_tickets_json()

        return ticket_id


    # =====================================================
    # BUSCAR UM TICKET
    # =====================================================

    @staticmethod
    def buscar_ticket(
        ticket_id
    ):

        chave = f"ticket:{ticket_id}"

        if not r.exists(chave):
            return None

        return r.hgetall(
            chave
        )


    # =====================================================
    # LISTAR TODOS OS TICKETS
    # =====================================================

    @staticmethod
    def listar_tickets():

        tickets = []

        for chave in r.keys(
            "ticket:*"
        ):

            dados = r.hgetall(
                chave
            )

            tickets.append(
                dados
            )

        return tickets


    # =====================================================
    # ATUALIZAR TICKET
    # =====================================================

    @staticmethod
    def atualizar_ticket(
        ticket_id,
        novos_dados
    ):

        chave = f"ticket:{ticket_id}"

        if not r.exists(
            chave
        ):
            return False

        r.hset(
            chave,
            mapping=novos_dados
        )

        RedisService.salvar_tickets_json()

        return True


    # =====================================================
    # DELETAR TICKET
    # =====================================================

    @staticmethod
    def deletar_ticket(
        ticket_id
    ):

        chave = f"ticket:{ticket_id}"

        if not r.exists(
            chave
        ):
            return False

        r.delete(
            chave
        )
        RedisService.salvar_tickets_json()

        return True
    
        # =====================================================
    # SALVAR TICKETS EM JSON
    # =====================================================

    @staticmethod
    def salvar_tickets_json():

        print("🔥 tentando salvar tickets")
        tickets = []

        for chave in r.keys("ticket:*"):

            dados = r.hgetall(chave)

            ticket_limpo = {
                "id": dados["id"],
                "nome_corrida": dados["nome_corrida"],
                "nome_cavalo": dados["nome_cavalo"],
                "valor_pago": dados["valor_pago"],
                "odd": dados["odd"]
            }

            tickets.append(ticket_limpo)

        with open(
            "tickets.json",
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                tickets,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def carregar_tickets_json():

        import os
        import json

        if not os.path.exists("tickets.json"):
            return

        with open(
            "tickets.json",
            "r",
            encoding="utf-8"
        ) as arquivo:

            tickets = json.load(
                arquivo
            )

        # evita duplicar se já estiver no redis
        if r.exists("proximoTicketId"):
            return

        maior_id = 0

        for ticket in tickets:

            ticket_id = int(
                ticket["id"]
            )

            r.hset(
                f"ticket:{ticket_id}",
                mapping=ticket
            )

            if ticket_id > maior_id:
                maior_id = ticket_id

        r.set(
            "proximoTicketId",
            maior_id
        )           