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
from services.redis_service import RedisService
from tkinter import messagebox
from view.tickets_view import TicketsView
from services.api_service import listar_corridas
from view.corridas_finalizadas_view import CorridasFinalizadasView
from services.api_service import listar_corridas_finalizadas


from view.criar_corrida_view import CriarCorridaView

from services.api_service import (
    listar_corridas_ativas,
    buscar_corrida,
    listar_pistas,
    listar_cavalos,
    criar_corrida
)

from view.pesquisa_view import PesquisaView

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
        self.frame_atual.pack(fill="both", expand=True)

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

        dados = RedisService.autenticar(usuario, senha)

        if dados:
            self.usuario_logado = dados
            self.mostrar_lobby()
        else:
            messagebox.showerror("Erro", "Login inválido")
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

    def cadastrar_usuario(self, usuario, senha):

        criado = RedisService.criar_usuario(usuario, senha)

        if criado:
            messagebox.showinfo("Sucesso", "Usuário criado!")
            self.mostrar_login()
        else:
            messagebox.showerror("Erro", "Usuário já existe")

    # =====================================================
    # LOBBY
    # =====================================================
    def criar_corrida(self):

        print("Criar corrida clicado")

    def mostrar_lobby(self):
        self.corridas = listar_corridas_ativas()

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
    # CONFIGURAÇÕES
    # =====================================================

    def mostrar_configuracoes(self):

        frame = ConfiguracoesView(
            self.root,
            None,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)
        
    def salvar_config(self, tema, idioma, nivel_aposta):

        self.usuario_logado["tema"] = tema
        self.usuario_logado["idioma"] = idioma
        self.usuario_logado["nivel_aposta"] = nivel_aposta

        Usuario.salvar_config(
            tema,
            idioma,
            nivel_aposta
        )

        messagebox.showinfo(
            "Sucesso",
            "Configurações salvas!"
        )

    def mostrar_corrida(self, corrida_id):

        from services.api_service import buscar_corrida

        corrida = buscar_corrida(corrida_id)

        frame = CorridaView(
            self.root,
            corrida,
            self.usuario_logado,
            self.apostar,
            self.mostrar_lobby,
        )

        self.trocar_frame(frame)

    def apostar(
        self,
        valor,
        nome_corrida,
        nome_cavalo,
        odd
    ):

        saldo_atual = float(
            self.usuario_logado["saldo"]
        )

        saldo_atual -= valor

        self.usuario_logado["saldo"] = saldo_atual

        RedisService.atualizar_saldo(
            self.usuario_logado["id"],
            saldo_atual
        )

        # salva ticket
        RedisService.criar_ticket(
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

    def mostrar_banco(self):

        frame = BancoView(
            self.root,
            self.usuario_logado,
            self.depositar,
            self.sacar,
            self.mostrar_lobby,
        )

        self.trocar_frame(frame)

    def depositar(self, valor):

        saldo_atual = float(self.usuario_logado["saldo"])

        saldo_atual += valor

        self.usuario_logado["saldo"] = saldo_atual

        RedisService.atualizar_saldo(
            self.usuario_logado["id"],
            saldo_atual
        )

        self.mostrar_lobby()
            
    def sacar(self, valor):

        saldo_atual = float(self.usuario_logado["saldo"])

        saldo_atual -= valor

        self.usuario_logado["saldo"] = saldo_atual

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
        
    def mostrar_corridas_finalizadas(self):

        corridas = listar_corridas_finalizadas()

        frame = CorridasFinalizadasView(
            self.root,
            corridas,
            self.mostrar_lobby
        )

        self.trocar_frame(frame)

    # =====================================================
    # PESQUISA
    # =====================================================

    def mostrar_pesquisa(self):

        frame = PesquisaView(
            self.root,
            self.registrar_pesquisa,
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
    def registrar_pesquisa(self, texto):

        Usuario.salvar_pesquisa(
        self.usuario_logado["usuario"],
        texto
    )
        
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
