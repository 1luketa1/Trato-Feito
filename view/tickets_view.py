import tkinter as tk


class TicketsView(tk.Frame):

    def __init__(
        self,
        master,
        tickets,
        voltar_callback
    ):
        super().__init__(master)

        # =========================
        # BOTÃO VOLTAR
        # =========================
        tk.Button(
            self,
            text="← Voltar",
            command=voltar_callback
        ).place(
            x=10,
            y=10
        )

        # =========================
        # TÍTULO
        # =========================
        tk.Label(
            self,
            text="🎫 Tickets",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        # =========================
        # SEM TICKETS
        # =========================
        if not tickets:
            tk.Label(
                self,
                text="Nenhum ticket encontrado."
            ).pack(pady=30)
            return

        # =========================
        # LISTA
        # =========================
        for ticket in tickets:

            texto = f"""
ID: {ticket['id']}
Corrida: {ticket['nome_corrida']}
Cavalo: {ticket['nome_cavalo']}
Valor Pago: R$ {ticket['valor_pago']}
Odd: {ticket['odd']}
            """

            tk.Label(
                self,
                text=texto,
                justify="left",
                relief="solid",
                padx=10,
                pady=8,
                anchor="w"
            ).pack(
                fill="x",
                padx=20,
                pady=5
            )