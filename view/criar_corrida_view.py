import tkinter as tk
from tkinter import messagebox


class CriarCorridaView(tk.Frame):

    def __init__(
        self,
        master,
        pistas,
        cavalos,
        criar_callback,
        voltar_callback
    ):

        super().__init__(master)

        self.cavalos = cavalos

        tk.Label(
            self,
            text="Criar Corrida",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # =====================================================
        # NOME
        # =====================================================

        tk.Label(self, text="Nome da corrida").pack()

        self.nome = tk.Entry(self, width=40)
        self.nome.pack(pady=5)

        # =====================================================
        # DATA
        # =====================================================

        tk.Label(self, text="Data (AAAA-MM-DD)").pack()

        self.data = tk.Entry(self, width=40)
        self.data.pack(pady=5)

        # =====================================================
        # PISTA
        # =====================================================

        tk.Label(self, text="Pista").pack()

        nomes_pistas = [
            pista["nome"]
            for pista in pistas
        ]

        self.pista_var = tk.StringVar(
            value=nomes_pistas[0]
            if nomes_pistas else ""
        )

        tk.OptionMenu(
            self,
            self.pista_var,
            *nomes_pistas
        ).pack(pady=5)

        # =====================================================
        # CAVALOS
        # =====================================================

        tk.Label(
            self,
            text="Selecione os cavalos"
        ).pack(pady=10)

        self.cavalos_vars = []

        for cavalo in cavalos:

            var = tk.BooleanVar()

            self.cavalos_vars.append(
                (var, cavalo)
            )

            tk.Checkbutton(
                self,
                text=cavalo["nome"],
                variable=var
            ).pack(anchor="w", padx=250)

        # =====================================================
        # BOTÕES
        # =====================================================

        def criar_corrida():

            nome = self.nome.get()
            data = self.data.get()

            pista_escolhida = None

            for pista in pistas:

                if pista["nome"] == self.pista_var.get():

                    pista_escolhida = pista

                    break

            cavalos_selecionados = []

            for var, cavalo in self.cavalos_vars:

                if var.get():

                    cavalos_selecionados.append(
                        cavalo["_id"]
                    )

            if len(cavalos_selecionados) < 2:

                messagebox.showerror(
                    "Erro",
                    "Selecione pelo menos 2 cavalos"
                )

                return

            dados = {
                "nome": nome,
                "data": data,
                "pista_id": pista_escolhida["_id"],
                "cavalos": cavalos_selecionados,
                "resultado": [],
                "status": "ativa"
            }

            criar_callback(dados)

        tk.Button(
            self,
            text="Criar Corrida",
            width=25,
            command=criar_corrida
        ).pack(pady=20)

        tk.Button(
            self,
            text="Voltar",
            width=25,
            command=voltar_callback
        ).pack()