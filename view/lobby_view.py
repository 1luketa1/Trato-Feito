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
    corridas
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

        for corrida in corridas:

            tk.Button(
                self,
                text=f"{corrida['nome']} - {corrida['pista']['distancia']}km",
                width=30,
                height=2,
                command=lambda c=corrida:
                    corrida_callback(c["_id"])
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