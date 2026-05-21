import tkinter as tk
from tkinter import messagebox


class CadastroView(tk.Frame):

    def __init__(self, master, cadastro_callback, voltar_callback):
        super().__init__(master)

        tk.Label(self, text="Cadastro", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Label(self, text="Usuário").pack()
        self.user = tk.Entry(self, width=30)
        self.user.pack(pady=5)

        tk.Label(self, text="Senha").pack()
        self.senha = tk.Entry(self, show="*", width=30)
        self.senha.pack(pady=5)

        tk.Label(self, text="Confirmar Senha").pack()
        self.confirmar = tk.Entry(self, show="*", width=30)
        self.confirmar.pack(pady=5)

        def cadastrar():

            usuario = self.user.get()
            senha = self.senha.get()
            confirmar = self.confirmar.get()

            if usuario == "" or senha == "":
                messagebox.showerror("Erro", "Preencha todos os campos")
                return

            if senha != confirmar:
                messagebox.showerror("Erro", "As senhas não coincidem")
                return

            print("BOTÃO FOI CLICADO")

            cadastro_callback(usuario, senha)
        tk.Button(
            self,
            text="Cadastrar",
            width=20,
            command=cadastrar
        ).pack(pady=20)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack()