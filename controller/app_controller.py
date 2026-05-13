from model.usuario_model import Usuario
from services.api_service import listar_corridas_ativas

from view.login_view import LoginView
from view.cadastro_view import CadastroView
from view.lobby_view import LobbyView
from view.corrida_view import CorridaView
from view.banco_view import BancoView
from view.configuracoes_view import ConfiguracoesView

from tkinter import messagebox

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

        dados = Usuario.autenticar(usuario, senha)

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
            self.mostrar_login
        )

        self.trocar_frame(frame)

    # =====================================================
    # LOBBY
    # =====================================================
    def criar_corrida(self):

        print("Criar corrida clicado")

    def mostrar_lobby(self):
        self.corridas = listar_corridas_ativas()

        frame = LobbyView(
            self.root,
            self.usuario_logado,
            self.corridas,
            self.logout,
            self.mostrar_configuracoes,
            self.mostrar_banco,
            self.mostrar_corrida,
            self.mostrar_criar_corrida,
            self.mostrar_pesquisa,
            self.mostrar_corridas_finalizadas
        )

        self.trocar_frame(frame)

    # =====================================================
    # CONFIGURAÇÕES
    # =====================================================

    def mostrar_configuracoes(self):

        frame = ConfiguracoesView(
            self.root,
            self.usuario_logado,
            self.salvar_config,
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

    def apostar(self, valor):

        self.usuario_logado["saldo"] -= valor


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

        self.usuario_logado["saldo"] += valor

    def sacar(self, valor):

        self.usuario_logado["saldo"] -= valor

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
