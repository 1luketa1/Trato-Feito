import tkinter as tk
from tkinter import messagebox


class CadastroView(tk.Frame):

    def __init__(self, master, voltar_callback):

        super().__init__(master)

        tk.Label(
            self,
            text="Cadastro",
            font=("Arial", 24, "bold")
        ).pack(pady=30)

        tk.Label(self, text="Usuário").pack()

        self.user = tk.Entry(self)
        self.user.pack()

        tk.Label(self, text="Senha").pack()

        self.senha = tk.Entry(self, show="*")
        self.senha.pack()

        tk.Label(self, text="Confirmar senha").pack()

        self.confirmar = tk.Entry(self, show="*")
        self.confirmar.pack()

        def cadastrar():

            if self.senha.get() != self.confirmar.get():

                messagebox.showerror(
                    "Erro",
                    "As senhas não coincidem"
                )

                return

            messagebox.showinfo(
                "Cadastro",
                "Usuário cadastrado!"
            )

            voltar_callback()

        tk.Button(
            self,
            text="Cadastrar",
            width=20,
            command=cadastrar
        ).pack(pady=15)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack()