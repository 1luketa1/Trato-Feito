from model.usuario_model import Usuario

from view.login_view import LoginView
from view.cadastro_view import CadastroView
from view.lobby_view import LobbyView
from view.corrida_view import CorridaView
from view.banco_view import BancoView
from view.configuracoes_view import ConfiguracoesView


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

    def mostrar_lobby(self):

        frame = LobbyView(
            self.root,
            self.usuario_logado,
            self.logout,
            self.mostrar_configuracoes,
            self.mostrar_banco,
            self.mostrar_corrida
        )

        self.trocar_frame(frame)

    # =====================================================
    # CONFIGURACOES
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

        messagebox.showinfo(
            "Sucesso",
            "Configurações salvas!"
        )

    # =====================================================
    # CORRIDAS
    # =====================================================

    def mostrar_corrida(self, numero):

        frame = CorridaView(
            self.root,
            numero,
            self.usuario_logado,
            self.apostar,
            self.mostrar_lobby,
        )

        self.trocar_frame(frame)

    def apostar(self, valor):

        self.usuario_logado["saldo"] -= valor

    # =====================================================
    # BANCO
    # =====================================================

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