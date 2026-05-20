import tkinter as tk
from tkinter import messagebox

from services.NeoService import (
    CreateViewedRunRelation,
    CreateFavoriteHorseRelation,
    CreateFavoriteTrackRelation
)

from database import (
    corridas_collection,
    pistas_collection,
    cavalos_collection
)

from bson import ObjectId


#Esta em View.Run
class RunDetailsView(tk.Frame):

    def __init__(
        self,
        master,
        run_id,
        usuario_id
    ):

        super().__init__(master)

        self.run_id = run_id
        self.usuario_id = usuario_id

        # =====================================
        # REGISTRA VISUALIZAÇÃO NO NEO4J
        # =====================================

        CreateViewedRunRelation(
            personDBAcessKey=str(usuario_id),
            runDBAcessKey=str(run_id)
        )

        # =====================================
        # BUSCA RUN
        # =====================================

        self.run = corridas_collection.find_one({
            "_id": ObjectId(run_id)
        })

        if not self.run:

            tk.Label(
                self,
                text="Corrida não encontrada",
                font=("Arial", 20, "bold")
            ).pack(pady=30)

            return

        # =====================================
        # PISTA
        # =====================================

        self.track = pistas_collection.find_one({
            "_id": self.run["pista_id"]
        })

        # =====================================
        # TÍTULO
        # =====================================

        tk.Label(
            self,
            text="Detalhes da Corrida",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # =====================================
        # DATA
        # =====================================

        tk.Label(
            self,
            text=f"Data: {self.run['data']}",
            font=("Arial", 12)
        ).pack(pady=5)

        # =====================================
        # STATUS
        # =====================================

        tk.Label(
            self,
            text=f"Status: {self.run.get('status', 'desconhecido')}",
            font=("Arial", 12)
        ).pack(pady=5)

        # =====================================
        # PISTA
        # =====================================

        pista_frame = tk.LabelFrame(
            self,
            text="Pista",
            padx=15,
            pady=15
        )

        pista_frame.pack(
            pady=15,
            padx=20,
            fill="x"
        )

        tk.Label(
            pista_frame,
            text=f"Nome: {self.track.get('nome', 'Sem nome')}",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Button(
            pista_frame,
            text="Favoritar Pista",
            command=self.favoritar_pista
        ).pack(
            pady=10,
            anchor="w"
        )

        # =====================================
        # CAVALOS
        # =====================================

        cavalos_frame = tk.LabelFrame(
            self,
            text="Cavalos",
            padx=15,
            pady=15
        )

        cavalos_frame.pack(
            pady=15,
            padx=20,
            fill="both",
            expand=True
        )

        for cavalo_id in self.run["cavalos"]:

            cavalo = cavalos_collection.find_one({
                "_id": cavalo_id
            })

            if not cavalo:
                continue

            item = tk.Frame(cavalos_frame)

            item.pack(
                fill="x",
                pady=8
            )

            tk.Label(
                item,
                text=cavalo.get(
                    "nome",
                    "Sem nome"
                ),
                font=("Arial", 12)
            ).pack(
                side="left",
                padx=10
            )

            tk.Button(
                item,
                text="Favoritar Cavalo",
                command=lambda c=str(cavalo["_id"]):
                    self.favoritar_cavalo(c)
            ).pack(
                side="left",
                padx=10
            )

            tk.Button(
                item,
                text="Comprar Ticket",
                command=lambda c=str(cavalo["_id"]):
                    self.comprar_ticket(c)
            ).pack(
                side="right",
                padx=10
            )

    # =====================================
    # FAVORITAR CAVALO
    # =====================================

    def favoritar_cavalo(self, cavalo_id):

        CreateFavoriteHorseRelation(
            personDBAcessKey=str(self.usuario_id),
            horseDBAcessKey=str(cavalo_id)
        )

        messagebox.showinfo(
            "Sucesso",
            "Cavalo favoritado"
        )

    # =====================================
    # FAVORITAR PISTA
    # =====================================

    def favoritar_pista(self):

        CreateFavoriteTrackRelation(
            personDBAcessKey=str(self.usuario_id),
            trackDBAcessKey=str(
                self.track["_id"]
            )
        )

        messagebox.showinfo(
            "Sucesso",
            "Pista favoritada"
        )

    # =====================================
    # COMPRAR TICKET
    # =====================================

    def comprar_ticket(self, cavalo_id):

        messagebox.showinfo(
            "Ticket",
            "Sistema de compra ainda não implementado"
        )