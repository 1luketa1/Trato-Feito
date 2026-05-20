import tkinter as tk
from tkinter import messagebox


class PesquisaView(tk.Frame):

    def __init__(
        self,
        master,
        pesquisar_callback,
        voltar_callback
    ):

        super().__init__(master)

        tk.Label(
            self,
            text="Pesquisa",
            font=("Arial", 24, "bold")
        ).pack(pady=30)

        tk.Label(
            self,
            text="Digite sua pesquisa"
        ).pack()

        self.entry_pesquisa = tk.Entry(
            self,
            width=40
        )

        self.entry_pesquisa.pack(pady=10)

        def pesquisar():

            texto = self.entry_pesquisa.get()

            if texto == "":

                messagebox.showerror(
                    "Erro",
                    "Digite algo"
                )

                return

            pesquisar_callback(texto)


        tk.Button(
            self,
            text="Buscar",
            width=20,
            command=pesquisar
        ).pack(pady=10)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack(pady=5)