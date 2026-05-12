import tkinter as tk


class LobbyView(tk.Frame):

    def __init__(
        self,
        master,
        usuario,
        logout_callback,
        config_callback,
        banco_callback,
        corrida_callback,
        pesquisa_callback
    ):

        super().__init__(master)

        tk.Label(
            self,
            text=f"Bem-vindo a CarlinhosBET",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        tk.Label(
            self,
            text=f"Saldo: R$ {usuario['saldo']:.2f}",
            font=("Arial", 18)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Corrida 1",
            width=30,
            height=2,
            command=lambda: corrida_callback(1)
        ).pack(pady=5)

        tk.Button(
            self,
            text="Corrida 2",
            width=30,
            height=2,
            command=lambda: corrida_callback(2)
        ).pack(pady=5)

        tk.Button(
            self,
            text="Corrida 3",
            width=30,
            height=2,
            command=lambda: corrida_callback(3)
        ).pack(pady=5)

        tk.Button(
            self,
            text="Carteira",
            width=30,
            height=2,
            command=banco_callback
        ).pack(pady=5)

        tk.Button(
            self,
            text="Configurações",
            width=30,
            height=2,
            command=config_callback
        ).pack(pady=5)

        tk.Button(
            self,
            text="Logout",
            width=30,
            height=2,
            command=logout_callback
        ).pack(pady=20)

        tk.Button(
            self,
            text="🔍",
            font=("Arial", 18),
            width=3,
            height=1,
            command=pesquisa_callback
        ).place(
                relx=0.88,
                rely=0.84
        )
