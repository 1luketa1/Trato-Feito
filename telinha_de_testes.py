import tkinter as tk
from tkinter import messagebox

# --------- LÓGICA (simulada) ---------
def autenticar(usuario, senha):
    if usuario == "admin" and senha == "123":
        return {"usuario": usuario, "saldo": 1500.75}
    return None


# --------- INTERFACE ---------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Apostas")
        self.root.geometry("300x250")

        self.frame_atual = None
        self.usuario_logado = None

        self.mostrar_login()

    # --------- CONTROLE DE TELA ---------
    def trocar_frame(self, novo_frame):
        if self.frame_atual is not None:
            self.frame_atual.destroy()  

        self.frame_atual = novo_frame
        self.frame_atual.pack(fill="both", expand=True)

    # --------- LOGIN ---------
    def mostrar_login(self):
        frame = tk.Frame(self.root)

        tk.Label(frame, text="Usuário").pack(pady=5)
        entry_user = tk.Entry(frame)
        entry_user.pack(pady=5)

        tk.Label(frame, text="Senha").pack(pady=5)
        entry_pass = tk.Entry(frame, show="*")
        entry_pass.pack(pady=5)

        def fazer_login():
            usuario = entry_user.get()
            senha = entry_pass.get()

            dados = autenticar(usuario, senha)

            if dados:
                self.usuario_logado = dados
                self.mostrar_lobby()
            else:
                messagebox.showerror("Erro", "Login inválido")

        tk.Button(frame, text="Entrar", command=fazer_login).pack(pady=10)

        self.trocar_frame(frame)

    # --------- LOBBY ---------
    def mostrar_lobby(self):
        frame = tk.Frame(self.root)

        nome = self.usuario_logado["usuario"]
        saldo = self.usuario_logado["saldo"]

        tk.Label(frame, text=f"Bem-vindo, {nome}!", font=("Arial", 14)).pack(pady=10)
        tk.Label(frame, text=f"Saldo: R$ {saldo:.2f}", font=("Arial", 12)).pack(pady=10)

        tk.Button(frame, text="Logout", command=self.mostrar_login).pack(pady=5)
        tk.Button(frame, text="Fechar App", command=self.root.destroy).pack(pady=5)

        self.trocar_frame(frame)


# --------- EXECUCAO ---------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
