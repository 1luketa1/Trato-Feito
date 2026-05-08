import tkinter as tk
from tkinter import messagebox


class CorridaView(tk.Frame):

    def __init__(
        self,
        master,
        numero,
        usuario,
        aposta_callback,
        voltar_callback,
    ):

        super().__init__(master)

        tk.Label(
            self,
            text=f"Corrida {numero}",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        cavalos = [
            "Filho da puta",
            "Black Nigger",
            "Golden Shower",
            "Silver Chariot",
            "Night Gunner"
        ]

        self.cavalo = tk.StringVar(value=cavalos[0])

        for cavalo in cavalos:

            tk.Radiobutton(
                self,
                text=cavalo,
                variable=self.cavalo,
                value=cavalo
            ).pack(anchor="w", padx=250)

        tk.Label(
            self,
            text=f"Saldo: R$ {usuario['saldo']:.2f}"
        ).pack(pady=10)

        tk.Label(
            self,
            text="Valor da aposta"
        ).pack()

        self.valor = tk.Entry(self)
        self.valor.pack()

        def apostar():

            try:

                valor = float(self.valor.get())

                if valor <= 0:
                    raise ValueError

                if valor > usuario["saldo"]:

                    messagebox.showerror(
                        "Erro",
                        "Saldo insuficiente"
                    )

                    return

                aposta_callback(valor)

                messagebox.showinfo(
                    "Aposta",
                    f"""
Aposta realizada!

Cavalo:
{self.cavalo.get()}

Valor:
R$ {valor:.2f}
                    """
                )

                voltar_callback()

            except:

                messagebox.showerror(
                    "Erro",
                    "Valor inválido"
                )

        tk.Button(
            self,
            text="Apostar",
            width=20,
            command=apostar
        ).pack(pady=10)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack(pady=5)
