import tkinter as tk
from tkinter import messagebox

from services.odds_services import gerar_odds_corrida
from services.api_service import simular_corrida
from services.redis_service import RedisService



class CorridaView(tk.Frame):

    def __init__(
        self,
        master,
        corrida,
        usuario,
        aposta_callback,
        voltar_callback,
        pagar_callback,
    ):

        super().__init__(master)

        odds_data = gerar_odds_corrida(corrida["_id"])
        odds = odds_data["odds"] if odds_data else {}

        tk.Label(
            self,
            text=corrida["nome"],
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        pista = corrida["pista"]

        tk.Label(
            self,
            text=f"""
Pista: {pista['nome']}
Tipo: {pista['tipo']}
Distância: {pista['distancia']} km
            """
        ).pack(pady=10)

        self.cavalo = tk.StringVar()

        self.mapa_cavalos = {} 

        for cavalo in corrida["cavalos"]:

            cavalo_id = cavalo["_id"]
            self.mapa_cavalos[cavalo_id] = cavalo["nome"]

            odd = odds.get(cavalo_id, 1.0)

            tk.Radiobutton(
                self,
                text=f"""
{cavalo['nome']}
Odd: {odd:.2f}
Velocidade Média: {cavalo['estatisticas']['velocidade_media']}
Resistência: {cavalo['estatisticas']['resistencia']}
                """,
                variable=self.cavalo,
                value=cavalo_id 
            ).pack(anchor="w", padx=80)


        tk.Label(
            self,
            text=f"Saldo: R$ {usuario['saldo']:.2f}"
        ).pack(pady=10)

        tk.Label(self, text="Valor da aposta").pack()

        self.valor = tk.Entry(self)
        self.valor.pack()

        def apostar():

            try:

                if not self.cavalo.get():
                    messagebox.showerror(
                        "Erro",
                        "Selecione um cavalo"
                    )
                    return

                valor = float(
                    self.valor.get()
                )

                if valor <= 0:
                    raise ValueError

                if valor > usuario["saldo"]:

                    messagebox.showerror(
                        "Erro",
                        "Saldo insuficiente"
                    )
                    return

                nome_cavalo = self.mapa_cavalos[
                    self.cavalo.get()
                ]

                odd = odds.get(
                    self.cavalo.get(),
                    1.0
                )

                aposta_callback(
                    valor,
                    corrida["_id"],
                    corrida["nome"],
                    self.cavalo.get(), 
                    nome_cavalo,
                    odd
                )

                nome_cavalo = self.mapa_cavalos[self.cavalo.get()]

                messagebox.showinfo(
                    "Aposta",
                    f"""
Aposta realizada!

Corrida: {corrida['nome']}
Cavalo: {nome_cavalo}
Valor: R$ {valor:.2f}
Odd: {odd:.2f}
                    """
                )

                voltar_callback()

            except:
                messagebox.showerror(
                    "Erro",
                    "Valor inválido"
                )

        def simular():

            resultado = simular_corrida(corrida["_id"])

            if not resultado or "erro" in resultado:
                messagebox.showerror("Erro", "Falha na simulação")
                return

            vencedor_id = resultado["vencedor"]
            nome_vencedor = self.mapa_cavalos.get(vencedor_id, vencedor_id)
            pagar_callback(corrida["_id"], vencedor_id)
            
            RedisService.pagar_apostas(
                corrida["_id"],
                vencedor_id   
            )

            texto_resultado = f"🏆 Vencedor: {nome_vencedor}\n\n"

            for r in resultado["resultado"]:
                nome = self.mapa_cavalos.get(r["cavalo_id"], r["cavalo_id"])

                texto_resultado += (
                    f"{r['posicao']}º - {nome} ({r['tempo']}s)\n"
                )

            messagebox.showinfo("Resultado da Corrida", texto_resultado)

            voltar_callback()

        tk.Button(
            self,
            text="Apostar",
            width=20,
            command=apostar
        ).pack(pady=10)

        tk.Button(
            self,
            text="Simular Corrida",
            width=20,
            command=simular
        ).pack(pady=10)

        tk.Button(
            self,
            text="Voltar",
            width=20,
            command=voltar_callback
        ).pack(pady=5)