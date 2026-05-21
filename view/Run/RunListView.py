import tkinter as tk

from services.api_service import buscar_corrida

#Esta em View.Run usa esse mesmo
class RunListView(tk.Frame):

    def __init__(
        self,
        master,
        corridas_ids,
        abrir_corrida_callback,
        voltar_callback
    ):

        super().__init__(master)

        # ====================================
        # TÍTULO
        # ====================================

        tk.Label(
            self,
            text="Lista de Corridas",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # ====================================
        # SCROLL
        # ====================================

        canvas = tk.Canvas(self)

        scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=canvas.yview
        )

        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ====================================
        # LISTA DE CORRIDAS
        # ====================================

        for corrida_id in corridas_ids:

            corrida = buscar_corrida(corrida_id)

            if not corrida:
                continue

            frame_corrida = tk.Frame(
                scroll_frame,
                bd=2,
                relief="groove",
                padx=10,
                pady=10
            )

            frame_corrida.pack(
                fill="x",
                padx=10,
                pady=5
            )

            nome_corrida = corrida.get(
                "nome",
                "Sem nome"
            )

            data = corrida.get(
                "data",
                "Sem data"
            )

            pista_nome = "Sem pista"

            if "pista" in corrida:
                pista_nome = corrida["pista"].get(
                    "nome",
                    "Sem pista"
                )

            # ============================
            # INFORMAÇÕES
            # ============================

            tk.Label(
                frame_corrida,
                text=f"Corrida: {nome_corrida}",
                font=("Arial", 14, "bold")
            ).pack(anchor="w")

            tk.Label(
                frame_corrida,
                text=f"Data: {data}"
            ).pack(anchor="w")

            tk.Label(
                frame_corrida,
                text=f"Pista: {pista_nome}"
            ).pack(anchor="w")

            # ============================
            # BOTÃO DETALHES
            # ============================

            tk.Button(
                frame_corrida,
                text="Detalhes",
                command=lambda c=corrida_id:
                    abrir_corrida_callback(c)
            ).pack(
                anchor="e",
                pady=5
            )

        # ====================================
        # VOLTAR
        # ====================================

        tk.Button(
            self,
            text="Voltar",
            width=25,
            command=voltar_callback
        ).pack(pady=15)