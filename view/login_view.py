import tkinter as tk


class LoginView(tk.Frame):

    def __init__(self, master, login_callback, cadastro_callback):

        super().__init__(master)

        tk.Label(
            self,
            text="CarlinhosBET",
            font=("Arial", 28, "bold")
        ).pack(pady=30)

        tk.Label(self, text="Usuário").pack()

        self.entry_user = tk.Entry(self)
        self.entry_user.pack(pady=5)

        tk.Label(self, text="Senha").pack()

        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack(pady=5)

        tk.Button(
            self,
            text="Entrar",
            width=20,
            command=lambda: login_callback(
                self.entry_user.get(),
                self.entry_pass.get()
            )
        ).pack(pady=15)

        tk.Button(
            self,
            text="Cadastrar",
            width=20,
            command=cadastro_callback
        ).pack()

        tk.Label(
            self,
            text="Login teste: admin / 123"
        ).pack(pady=20)