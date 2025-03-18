import tkinter as tk
from tkinter import messagebox
from conexao import connect_db
import bcrypt

def criar_tela_cadastro():
    cadastro_window = tk.Tk()
    cadastro_window.title("Cadastro de Usuário")

    tk.Label(cadastro_window, text="Email").pack(pady=5)
    entry_email = tk.Entry(cadastro_window)
    entry_email.pack(pady=5)

    tk.Label(cadastro_window, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(cadastro_window, show="*")
    entry_senha.pack(pady=5)

    tk.Label(cadastro_window, text="Confirmar Senha").pack(pady=5)
    entry_confirmar_senha = tk.Entry(cadastro_window, show="*")
    entry_confirmar_senha.pack(pady=5)

    def cadastrar_usuario():
        email = entry_email.get()
        senha = entry_senha.get()
        confirmar_senha = entry_confirmar_senha.get()

        if not email or not senha or not confirmar_senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO usuarios (email, senha) VALUES (%s, %s)", (email, hashed_password))
                conn.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                cadastro_window.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
            finally:
                cursor.close()
                conn.close()

    tk.Button(cadastro_window, text="Cadastrar", command=cadastrar_usuario).pack(pady=5)

    tk.Button(cadastro_window, text="Voltar para Login", command=cadastro_window.destroy).pack(pady=5)

    cadastro_window.mainloop()