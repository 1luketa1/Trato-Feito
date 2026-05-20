import redis
import json

from services.NeoService import (
    CreatePerson,
    CreateTicket,
    UpdateTicketValue,
    DeleteTicket
)

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
        usuarioId = str(
            r.incr("proximoUsuarioId")
        )

        # salva no Redis
        r.hset(
            f"usuario:{usuarioId}",
            mapping={
                "id": usuarioId,
                "nome": nome,
                "senha": senha,
                "saldo": 0
            }
        )

        # salva no Neo4j
        CreatePerson(
            name=nome,
            dBAcessKey=usuarioId
        )

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
            return False

        r.hset(
            chave,
            "saldo",
            saldo
        )

        RedisService.salvar_json()

        return True

    # ===============================
    # SALVAR JSON
    # ===============================

    @staticmethod
    def salvar_json():

        usuarios = []

        for chave in r.keys("usuario:*"):

            usuarios.append(
                r.hgetall(chave)
            )

        with open(
            ARQUIVO,
            "w",
            encoding="utf-8"
        ) as f:

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

            with open(
                ARQUIVO,
                "r",
                encoding="utf-8"
            ) as f:

                usuarios = json.load(f)

            r.flushdb()

            maior_id = 0

            for usuario in usuarios:

                usuario_id = str(
                    usuario["id"]
                )

                r.hset(
                    f"usuario:{usuario_id}",
                    mapping=usuario
                )

                # recria no Neo4j
                CreatePerson(
                    name=usuario["nome"],
                    dBAcessKey=usuario_id
                )

                if int(usuario_id) > maior_id:
                    maior_id = int(usuario_id)

            r.set(
                "proximoUsuarioId",
                maior_id
            )

        except FileNotFoundError:
            pass

    # =====================================================
    # CRIAR TICKET
    # =====================================================

    @staticmethod
    def criar_ticket(
        usuario_id,
        corrida_id,
        cavalo_id,
        nome_corrida,
        nome_cavalo,
        valor_pago,
        odd
    ):

        ticket_id = str(
            r.incr("proximoTicketId")
        )

        r.hset(
            f"ticket:{ticket_id}",
            mapping={
                "id": ticket_id,
                "usuario_id": str(usuario_id),
                "corrida_id": str(corrida_id),
                "cavalo_id": str(cavalo_id),
                "nome_corrida": nome_corrida,
                "nome_cavalo": nome_cavalo,
                "valor_pago": valor_pago,
                "odd": odd
            }
        )

        # salva no Neo4j
        CreateTicket(
            value=float(valor_pago),
            buyerDBAcessKey=str(usuario_id),
            runDBAcessKey=str(corrida_id),
            horseBetDBAcessKey=str(cavalo_id),
            dBAcessKey=str(ticket_id)
        )

        RedisService.salvar_tickets_json()

        return ticket_id

    # =====================================================
    # BUSCAR TICKET
    # =====================================================

    @staticmethod
    def buscar_ticket(ticket_id):

        chave = f"ticket:{ticket_id}"

        if not r.exists(chave):
            return None

        return r.hgetall(chave)

    # =====================================================
    # LISTAR TICKETS
    # =====================================================

    @staticmethod
    def listar_tickets():

        tickets = []

        for chave in r.keys("ticket:*"):

            tickets.append(
                r.hgetall(chave)
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

        if not r.exists(chave):
            return False

        r.hset(
            chave,
            mapping=novos_dados
        )

        ticket = r.hgetall(chave)

        # atualiza valor no Neo4j
        if "valor_pago" in novos_dados:

            UpdateTicketValue(
                dBAcessKey=str(ticket_id),
                newValue=float(
                    ticket["valor_pago"]
                )
            )

        RedisService.salvar_tickets_json()

        return True

    # =====================================================
    # DELETAR TICKET
    # =====================================================

    @staticmethod
    def deletar_ticket(ticket_id):

        chave = f"ticket:{ticket_id}"

        if not r.exists(chave):
            return False

        # deleta no Neo4j
        DeleteTicket(
            dBAcessKey=str(ticket_id)
        )

        # deleta no Redis
        r.delete(chave)

        RedisService.salvar_tickets_json()

        return True

    # =====================================================
    # SALVAR TICKETS JSON
    # =====================================================

    @staticmethod
    def salvar_tickets_json():

        tickets = []

        for chave in r.keys("ticket:*"):

            dados = r.hgetall(chave)

            tickets.append({
                "id": dados["id"],
                "usuario_id": dados.get("usuario_id"),
                "corrida_id": dados.get("corrida_id"),
                "cavalo_id": dados.get("cavalo_id"),
                "nome_corrida": dados["nome_corrida"],
                "nome_cavalo": dados["nome_cavalo"],
                "valor_pago": dados["valor_pago"],
                "odd": dados["odd"]
            })

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

    # =====================================================
    # CARREGAR TICKETS JSON
    # =====================================================

    @staticmethod
    def carregar_tickets_json():

        import os

        if not os.path.exists(
            "tickets.json"
        ):
            return

        with open(
            "tickets.json",
            "r",
            encoding="utf-8"
        ) as arquivo:

            tickets = json.load(
                arquivo
            )

        maior_id = 0

        for ticket in tickets:

            ticket_id = str(
                ticket["id"]
            )

            r.hset(
                f"ticket:{ticket_id}",
                mapping=ticket
            )

            # recria no Neo4j
            CreateTicket(
                value=float(
                    ticket["valor_pago"]
                ),
                buyerDBAcessKey=str(
                    ticket["usuario_id"]
                ),
                runDBAcessKey=str(
                    ticket["corrida_id"]
                ),
                horseBetDBAcessKey=str(
                    ticket["cavalo_id"]
                ),
                dBAcessKey=ticket_id
            )

            if int(ticket_id) > maior_id:
                maior_id = int(ticket_id)

        r.set(
            "proximoTicketId",
            maior_id
        )
        
    @staticmethod
    def pagar_apostas(corrida_id, cavalo_vencedor_id):
        

        for chave in r.keys("ticket:*"):

            ticket = r.hgetall(chave)

            if ticket.get("corrida_id") != str(corrida_id):
                continue

            if ticket.get("cavalo_id") == cavalo_vencedor_id:

                usuario_id = ticket.get("usuario_id")

                if not usuario_id:
                    continue

                valor = float(ticket["valor_pago"])
                odd = float(ticket["odd"])

                premio = valor * odd

                
                user_key = f"usuario:{usuario_id}"
                saldo = float(r.hget(user_key, "saldo"))

                saldo += premio

                RedisService.atualizar_saldo(
                    usuario_id,
                    saldo
                )

        RedisService.salvar_json()