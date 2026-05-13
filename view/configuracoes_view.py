import tkinter as tk
from tkinter import messagebox
import json
import os


class ConfiguracoesView(tk.Frame):

    def __init__(
        self,
        master,
        salvar_callback,
        voltar_callback
    ):
        super().__init__(master)

        # ====================================
        # CARREGAR CONFIG LOCAL (config.json)
        # ====================================

        arquivo = "config.json"

        config = {
            "tema": "claro",
            "lingua": "pt",
            "nivel_aposta": "medio"
        }

        if os.path.exists(arquivo):
            with open(
                arquivo,
                "r",
                encoding="utf-8"
            ) as f:
                config.update(
                    json.load(f)
                )

        # ====================================
        # TÍTULO
        # ====================================

        tk.Label(
            self,
            text="Configurações",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # ====================================
        # TEMA
        # ====================================

        tk.Label(
            self,
            text="Tema"
        ).pack()

        self.tema_var = tk.StringVar(
            value=config["tema"]
        )

        tk.OptionMenu(
            self,
            self.tema_var,
            "claro",
            "escuro"
        ).pack(pady=5)

        # ====================================
        # LÍNGUA
        # ====================================

        tk.Label(
            self,
            text="Língua"
        ).pack()

        self.lingua_var = tk.StringVar(
            value=config["lingua"]
        )

        tk.OptionMenu(
            self,
            self.lingua_var,
            "pt",
            "en"
        ).pack(pady=5)

        # ====================================
        # NÍVEL DE APOSTA
        # ====================================

        tk.Label(
            self,
            text="Nível de Aposta"
        ).pack()

        self.nivel_var = tk.StringVar(
            value=config["nivel_aposta"]
        )

        tk.OptionMenu(
            self,
            self.nivel_var,
            "baixo",
            "medio",
            "alto"
        ).pack(pady=5)

        # ====================================
        # SALVAR
        # ====================================

        def salvar():

            novas_config = {
                "tema": self.tema_var.get(),
                "lingua": self.lingua_var.get(),
                "nivel_aposta": self.nivel_var.get()
            }

            with open(
                "config.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    novas_config,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            if salvar_callback:
                salvar_callback(
                    novas_config
                )

            messagebox.showinfo(
                "Sucesso",
                "Configurações salvas!"
            )

        # ====================================
        # BOTÕES
        # ====================================

        tk.Button(
            self,
            text="Salvar",
            width=20,
            command=salvar
        ).pack(pady=20)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack()