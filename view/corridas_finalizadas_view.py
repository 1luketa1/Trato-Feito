import tkinter as tk


class CorridasFinalizadasView(tk.Frame):

    def __init__(
        self,
        master,
        corridas,
        voltar_callback
    ):
        super().__init__(master)

        tk.Button(
            self,
            text="← Voltar",
            command=voltar_callback
        ).place(
            x=10,
            y=10
        )

        tk.Label(
            self,
            text="Corridas Finalizadas",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        for corrida in corridas:

            header = f"""
🏁 {corrida['nome']}
Pista: {corrida['pista']['nome']}
Status: {corrida['status']}
            """

            tk.Label(
                self,
                text=header,
                justify="left",
                font=("Arial", 12, "bold"),
                anchor="w"
            ).pack(fill="x", padx=20, pady=(10, 0))

            mapa_cavalos = {
                cavalo["_id"]: cavalo["nome"]
                for cavalo in corrida.get("cavalos", [])
            }

            resultados = sorted(
                corrida.get("resultado", []),
                key=lambda x: x["posicao"]
            )

            placar_texto = ""

            for r in resultados:

                nome = mapa_cavalos.get(
                    r["cavalo_id"],
                    "Desconhecido"
                )

                pos = r["posicao"]
                tempo = r["tempo"]

                if pos == 1:
                    medalha = "🥇"
                elif pos == 2:
                    medalha = "🥈"
                elif pos == 3:
                    medalha = "🥉"
                else:
                    medalha = f"{pos}º"

                placar_texto += (
                    f"{medalha} - {nome} "
                    f"({tempo:.2f}s)\n"
                )

            tk.Label(
                self,
                text=placar_texto,
                justify="left",
                relief="solid",
                padx=10,
                pady=5
            ).pack(fill="x", padx=20, pady=5)
