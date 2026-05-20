from model.usuario_model import Usuario
from services.api_service import listar_corridas_ativas
from services.redis_service import RedisService
from tkinter import messagebox

from view.login_view import LoginView
from view.cadastro_view import CadastroView
from view.lobby_view import LobbyView
from view.corrida_view import CorridaView
from view.banco_view import BancoView
from view.configuracoes_view import ConfiguracoesView
from view.tickets_view import TicketsView
from view.corridas_finalizadas_view import CorridasFinalizadasView
from view.criar_corrida_view import CriarCorridaView
from services.redis_service import r


# =========================================
# NOVAS VIEWS
# =========================================

from view.SearchView import SearchView
from view.Run.RunListView import RunListView
from view.Run.RunDetailsView import RunDetailsView

# =========================================
# API
# =========================================

from services.api_service import (
    listar_corridas_ativas,
    buscar_corrida,
    listar_pistas,
    listar_cavalos,
    criar_corrida,
    listar_corridas_finalizadas
)

# =========================================
# NEO4J FILTERS
# =========================================

from services.NeoService import *

class AppController:

    def __init__(self, root):

        self.root = root

        self.root.title("CarlinhosBet")
        self.root.geometry("700x500")

        self.frame_atual = None

        self.usuario_logado = None

        RedisService.carregar_json()
        RedisService.carregar_tickets_json()

        self.mostrar_login()

    # =====================================================
    # TROCA DE TELAS
    # =====================================================

    def trocar_frame(self, frame):

        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = frame

        self.frame_atual.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # LOGIN
    # =====================================================

    def mostrar_login(self):

        frame = LoginView(
            self.root,
            self.fazer_login,
            self.mostrar_cadastro
        )

        self.trocar_frame(frame)

    def fazer_login(self, usuario, senha):

        dados = RedisService.autenticar(
            usuario,
            senha
        )

        if dados:

            self.usuario_logado = dados

            self.mostrar_lobby()

        else:

            messagebox.showerror(
                "Erro",
                "Login inválido"
            )

    # =====================================================
    # CADASTRO
    # =====================================================

    def mostrar_cadastro(self):

        frame = CadastroView(
            self.root,
            self.cadastrar_usuario,
            self.mostrar_login
        )

        self.trocar_frame(frame)

    def cadastrar_usuario(
        self,
        usuario,
        senha
    ):

        criado = RedisService.criar_usuario(
            usuario,
            senha
        )

        if criado:

            messagebox.showinfo(
                "Sucesso",
                "Usuário criado!"
            )

            self.mostrar_login()

        else:

            messagebox.showerror(
                "Erro",
                "Usuário já existe"
            )

    # =====================================================
    # LOBBY
    # =====================================================

    def mostrar_lobby(self):

        corridas = listar_corridas_ativas()

        frame = LobbyView(
            self.root,
            self.usuario_logado,
            corridas,
            self.logout,
            self.mostrar_configuracoes,
            self.mostrar_banco,
            self.mostrar_corrida,
            self.mostrar_criar_corrida,
            self.mostrar_corridas_finalizadas,
            self.mostrar_tickets,
            self.mostrar_pesquisa
        )

        self.trocar_frame(frame)

    # =====================================================
    # CONFIG
    # =====================================================

    def mostrar_configuracoes(self):

        frame = ConfiguracoesView(
            self.root,
            None,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)

    # =====================================================
    # CORRIDA
    # =====================================================

    def mostrar_corrida(self, corrida_id):

        corrida = buscar_corrida(
            corrida_id
        )

        frame = CorridaView(
            self.root,
            corrida,
            self.usuario_logado,
            self.apostar,
            self.mostrar_lobby,
            self.pagar_apostas
        )

        self.trocar_frame(frame)

    # =====================================================
    # SEARCH VIEW
    # =====================================================

    def mostrar_pesquisa(self):

        frame = SearchView(
            self.root,
            self.abrir_lista_pesquisa,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)

    # =====================================================
    # ABRIR LISTA
    # =====================================================

    def abrir_lista_pesquisa(
        self,
        nome_filtro
    ):

        limite = 20

        usuario_id = str(
            self.usuario_logado["id"]
        )

        filtros = {

            # =====================================
            # ALL RUNS
            # =====================================

            "FilterByAllMostViewedRuns":
                lambda:
                    FilterByAllMostViewedRuns(
                        limite
                    ),

            "FilterByAllMostBuyedRuns":
                lambda:
                    FilterByAllMostBuyedRuns(
                        limite
                    ),

            "FilterByPersonFavoriteTracksAllRuns":
                lambda:
                    FilterByPersonFavoriteTracksAllRuns(
                        usuario_id,
                        limite
                    ),

            "FilterByPersonMostViewedTracksAllRuns":
                lambda:
                    FilterByPersonMostViewedTracksAllRuns(
                        usuario_id,
                        limite
                    ),

            "FilterByPersonFavoriteHorsesAllRuns":
                lambda:
                    FilterByPersonFavoriteHorsesAllRuns(
                        usuario_id,
                        limite
                    ),

            "FilterByPersonMostViewedHorsesAllRuns":
                lambda:
                    FilterByPersonMostViewedHorsesAllRuns(
                        usuario_id,
                        limite
                    ),

            # =====================================
            # OPEN RUNS
            # =====================================

            "FilterByMostViewedOpenRuns":
                lambda:
                    FilterByMostViewedOpenRuns(
                        limite
                    ),

            "FilterByOpenMostBuyedRuns":
                lambda:
                    FilterByOpenMostBuyedRuns(
                        limite
                    ),

            "FilterByPersonFavoriteTracksOpenRuns":
                lambda:
                    FilterByPersonFavoriteTracksOpenRuns(
                        usuario_id,
                        limite
                    ),

            "FilterByPersonMostViewedTracksOpenRuns":
                lambda:
                    FilterByPersonMostViewedTracksOpenRuns(
                        usuario_id,
                        limite
                    ),

            "FilterByPersonFavoriteHorsesOpenRuns":
                lambda:
                    FilterByPersonFavoriteHorsesOpenRuns(
                        usuario_id,
                        limite
                    ),

            "FilterByPersonMostViewedHorsesOpenRuns":
                lambda:
                    FilterByPersonMostViewedHorsesOpenRuns(
                        usuario_id,
                        limite
                    )
        }

        if nome_filtro not in filtros:

            messagebox.showerror(
                "Erro",
                "Filtro não encontrado"
            )

            return

        resultados = filtros[
            nome_filtro
        ]()

        corridas_ids = []

        for item in resultados:

            run = item["run"]

            corridas_ids.append(
                run["dBAcessKey"]
            )

        self.mostrar_lista_corridas(
            corridas_ids
        )

    # =====================================================
    # RUN LIST
    # =====================================================

    def mostrar_lista_corridas(
        self,
        corridas_ids
    ):

        frame = RunListView(
            self.root,
            corridas_ids,
            self.mostrar_detalhes_corrida,
            self.mostrar_pesquisa
        )

        self.trocar_frame(frame)

    # =====================================================
    # RUN DETAILS
    # =====================================================

    def mostrar_detalhes_corrida(
        self,
        corrida_id
    ):

        frame = RunDetailsView(
            self.root,
            corrida_id,
            self.usuario_logado["id"]
        )

        self.trocar_frame(frame)

    # =====================================================
    # BANCO
    # =====================================================

    def mostrar_banco(self):

        frame = BancoView(
            self.root,
            self.usuario_logado,
            self.depositar,
            self.sacar,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)

    # =====================================================
    # TICKETS
    # =====================================================

    def mostrar_tickets(self):

        tickets = RedisService.listar_tickets()

        frame = TicketsView(
            self.root,
            tickets,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)

    # =====================================================
    # FINALIZADAS
    # =====================================================

    def mostrar_corridas_finalizadas(self):

        corridas = listar_corridas_finalizadas()

        frame = CorridasFinalizadasView(
            self.root,
            corridas,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)

    # =====================================================
    # CRIAR CORRIDA
    # =====================================================

    def mostrar_criar_corrida(self):

        pistas = listar_pistas()

        cavalos = listar_cavalos()

        frame = CriarCorridaView(
            self.root,
            pistas,
            cavalos,
            self.salvar_corrida,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)

    def salvar_corrida(self, dados):

        criar_corrida(dados)

        messagebox.showinfo(
            "Sucesso",
            "Corrida criada!"
        )

        self.mostrar_lobby()

    # =====================================================
    # APOSTA
    # =====================================================

    def apostar(
        self,
        valor,
        corrida_id,
        nome_corrida,
        cavalo_id,
        nome_cavalo,
        odd
    ):

        saldo_atual = float(
            self.usuario_logado["saldo"]
        )

        saldo_atual -= valor

        self.usuario_logado[
            "saldo"
        ] = saldo_atual

        RedisService.atualizar_saldo(
            self.usuario_logado["id"],
            saldo_atual
        )

        RedisService.criar_ticket(
            self.usuario_logado["id"],
            corrida_id,
            cavalo_id,
            nome_corrida,
            nome_cavalo,
            valor,
            odd
        )

        messagebox.showinfo(
            "Aposta registrada",
            "Ticket salvo com sucesso!"
        )

        self.mostrar_lobby()


    def pagar_apostas(self, corrida_id, vencedor_id):

        RedisService.pagar_apostas(corrida_id, vencedor_id)

        for chave in r.keys("usuario:*"):

            usuario = r.hgetall(chave)

            if usuario.get("id") == str(self.usuario_logado["id"]):

                self.usuario_logado["saldo"] = float(usuario["saldo"])
                break

    # =====================================================
    # BANCO
    # =====================================================

    def depositar(self, valor):

        saldo_atual = float(
            self.usuario_logado["saldo"]
        )

        saldo_atual += valor

        self.usuario_logado[
            "saldo"
        ] = saldo_atual

        RedisService.atualizar_saldo(
            self.usuario_logado["id"],
            saldo_atual
        )

        self.mostrar_lobby()

    def sacar(self, valor):

        saldo_atual = float(
            self.usuario_logado["saldo"]
        )

        saldo_atual -= valor

        self.usuario_logado[
            "saldo"
        ] = saldo_atual

        RedisService.atualizar_saldo(
            self.usuario_logado["id"],
            saldo_atual
        )

        self.mostrar_lobby()

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        self.usuario_logado = None

        self.mostrar_login()