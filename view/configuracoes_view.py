import tkinter as tk


class ConfiguracoesView(tk.Frame):

    def __init__(
        self,
        master,
        usuario,
        salvar_callback,
        voltar_callback
    ):

        super().__init__(master)

        tk.Label(
            self,
            text="Configurações",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # =================================================
        # TEMA
        # =================================================

        tk.Label(
            self,
            text="Tema"
        ).pack()

        self.tema = tk.StringVar(
            value=usuario["tema"]
        )

        tk.OptionMenu(
            self,
            self.tema,
            "Claro",
            "Escuro"
        ).pack(pady=5)

        # =================================================
        # IDIOMA
        # =================================================

        tk.Label(
            self,
            text="Idioma"
        ).pack()

        self.idioma = tk.StringVar(
            value=usuario["idioma"]
        )

        tk.OptionMenu(
            self,
            self.idioma,
            "Português",
            "English",
        ).pack(pady=5)

        # =================================================
        # NÍVEL DE APOSTA
        # =================================================

        tk.Label(
            self,
            text="Nível de Aposta"
        ).pack()

        self.nivel_aposta = tk.StringVar(
            value=usuario.get("nivel_aposta", "Normal")
        )

        tk.OptionMenu(
            self,
            self.nivel_aposta,
            "Segura",
            "Normal",
            "Insana"
        ).pack(pady=5)

        # =================================================
        # BOTÕES
        # =================================================

        tk.Button(
            self,
            text="Salvar",
            width=20,
            command=lambda: salvar_callback(
                self.tema.get(),
                self.idioma.get(),
                self.nivel_aposta.get()
            )
        ).pack(pady=20)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack()