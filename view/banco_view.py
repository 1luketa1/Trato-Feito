import tkinter as tk
from tkinter import messagebox


class BancoView(tk.Frame):

    def __init__(
        self,
        master,
        usuario,
        depositar_callback,
        sacar_callback,
        voltar_callback,
    ):

        super().__init__(master)

        tk.Label(
            self,
            text="Carteira",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        tk.Label(
            self,
            text=f"Saldo: R$ {usuario['saldo']:.2f}",
            font=("Arial", 18)
        ).pack(pady=10)

        tk.Label(
            self,
            text="Valor"
        ).pack()

        self.valor = tk.Entry(self)
        self.valor.pack()

        def depositar():

            try:

                valor = float(self.valor.get())

                depositar_callback(valor)

                messagebox.showinfo(
                    "Depósito",
                    f"Depósito de R$ {valor:.2f} realizado!"
                )

                voltar_callback()

            except:

                messagebox.showerror(
                    "Erro",
                    "Valor inválido"
                )

        def sacar():

            try:

                valor = float(self.valor.get())

                if valor > usuario["saldo"]:

                    messagebox.showerror(
                        "Erro",
                        "Saldo insuficiente"
                    )

                    return

                sacar_callback(valor)

                messagebox.showinfo(
                    "Saque",
                    f"Saque de R$ {valor:.2f} realizado!"
                )

                voltar_callback()

            except:

                messagebox.showerror(
                    "Erro",
                    "Valor inválido"
                )

        tk.Button(
            self,
            text="Depositar",
            width=20,
            command=depositar
        ).pack(pady=5)

        tk.Button(
            self,
            text="Sacar",
            width=20,
            command=sacar
        ).pack(pady=5)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack(pady=5)
