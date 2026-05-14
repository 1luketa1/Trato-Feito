import tkinter as tk


#Esta em View
class SearchView(tk.Frame):

    def __init__(
        self,
        master,
        abrir_lista_callback,
        voltar_callback
    ):

        super().__init__(master)

        # =========================================
        # TÍTULO
        # =========================================

        tk.Label(
            self,
            text="Pesquisa Inteligente",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # =========================================
        # PERSON HORSES
        # =========================================

        tk.Label(
            self,
            text="Person Horses",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Cavalos Favoritos",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonFavoriteHorses"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Cavalos Mais Visualizados",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonMostViewedHorses"
            )
        ).pack(pady=2)

        # =========================================
        # PERSON TRACKS
        # =========================================

        tk.Label(
            self,
            text="Person Tracks",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Pistas Favoritas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonFavoriteTracks"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Pistas Mais Visualizadas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonMostViewedTracks"
            )
        ).pack(pady=2)

        # =========================================
        # ALL RUNS
        # =========================================

        tk.Label(
            self,
            text="All Runs",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Corridas Mais Visualizadas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByAllMostViewedRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Corridas Mais Compradas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByAllMostBuyedRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Corridas das Pistas Favoritas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonFavoriteTracksAllRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Corridas das Pistas Mais Visualizadas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonMostViewedTracksAllRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Corridas dos Cavalos Favoritos",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonFavoriteHorsesAllRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Corridas dos Cavalos Mais Visualizados",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonMostViewedHorsesAllRuns"
            )
        ).pack(pady=2)

        # =========================================
        # OPEN RUNS
        # =========================================

        tk.Label(
            self,
            text="Open Runs",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Open Runs Mais Visualizadas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByMostViewedOpenRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Open Runs Mais Compradas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByOpenMostBuyedRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Open Runs das Pistas Favoritas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonFavoriteTracksOpenRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Open Runs das Pistas Mais Visualizadas",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonMostViewedTracksOpenRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Open Runs dos Cavalos Favoritos",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonFavoriteHorsesOpenRuns"
            )
        ).pack(pady=2)

        tk.Button(
            self,
            text="Open Runs dos Cavalos Mais Visualizados",
            width=40,
            command=lambda: abrir_lista_callback(
                "FilterByPersonMostViewedHorsesOpenRuns"
            )
        ).pack(pady=2)

        # =========================================
        # VOLTAR
        # =========================================

        tk.Button(
            self,
            text="Voltar",
            width=30,
            command=voltar_callback
        ).pack(pady=20)