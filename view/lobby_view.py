import tkinter as tk


class LobbyView(tk.Frame):

    def __init__(
        self,
        master,
        usuario,
        corridas,
        logout_callback,
        config_callback,
        banco_callback,
        corrida_callback,
        criar_corrida_callback,
        mostrar_corridas_finalizadas_callback,
        tickets_callback,
        pesquisa_callback
    ):

        super().__init__(master)

        tk.Label(
            self,
            text="CarlinhosBET",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.saldo_var = tk.StringVar()
        self.saldo_var.set(f"Saldo: R$ {usuario['saldo']:.2f}")

        tk.Label(
            self,
            textvariable=self.saldo_var,
            font=("Arial", 18)
        ).pack(pady=10)

        tk.Label(
            self,
            text="Corridas Ativas",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        for corrida in corridas:

            texto = (
                f"{corrida['nome']} | "
                f"{corrida['pista']['nome']} | "
                f"{corrida['status']}"
            )

            tk.Button(
                self,
                text=texto,
                width=50,
                height=2,
                command=lambda c=corrida:
                    corrida_callback(c["_id"])
            ).pack(pady=5)

        tk.Button(
            self,
            text="Criar Corrida",
            width=30,
            height=2,
            command=criar_corrida_callback
        ).pack(pady=15)
        
        tk.Button(
            self,
            text="Corridas Finalizadas",
            command=mostrar_corridas_finalizadas_callback,
            width=25
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
            text="🎫",
            font=("Arial", 18),
            width=3,
            height=1,
            command=tickets_callback
        ).place(
            relx=0.88,
            rely=0.72
        )

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
    def atualizar_saldo(self, novo_saldo):
        self.saldo_var.set(f"Saldo: R$ {novo_saldo:.2f}")