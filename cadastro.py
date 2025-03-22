import tkinter as tk
from tkinter import messagebox
from conexao import connect_db
import bcrypt

def criar_tela_cadastro(login_window):
    cadastro_window = tk.Toplevel(login_window)  
    cadastro_window.title("Cadastro de Usuário")

    cadastro_window.state('zoomed')

    frame = tk.Frame(cadastro_window)
    frame.pack(expand=True)

    label_font = ("Arial", 16)
    entry_font = ("Arial", 14)

    tk.Label(frame, text="Nome", font=label_font).pack(pady=10)
    entry_nome = tk.Entry(frame, font=entry_font, width=30)
    entry_nome.pack(pady=10)

    tk.Label(frame, text="Email", font=label_font).pack(pady=10)
    entry_email = tk.Entry(frame, font=entry_font, width=30)
    entry_email.pack(pady=10)

    tk.Label(frame, text="Senha", font=label_font).pack(pady=10)
    entry_senha = tk.Entry(frame, font=entry_font, show="*", width=30)
    entry_senha.pack(pady=10)

    tk.Label(frame, text="Confirmar Senha", font=label_font).pack(pady=10)
    entry_confirmar_senha = tk.Entry(frame, font=entry_font, show="*", width=30)
    entry_confirmar_senha.pack(pady=10)

    def cadastrar_usuario():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        confirmar_senha = entry_confirmar_senha.get()

        if not nome or not email or not senha or not confirmar_senha:
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
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", 
                               (nome, email, hashed_password))
                conn.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                cadastro_window.destroy()  
                login_window.deiconify()  
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
            finally:
                cursor.close()
                conn.close()

    tk.Button(frame, text="Cadastrar", command=cadastrar_usuario, font=("Arial", 14), width=20, height=2).pack(pady=10)

    tk.Button(frame, text="Voltar para Login", command=lambda: (cadastro_window.destroy(), login_window.deiconify()), font=("Arial", 14), width=20, height=2).pack(pady=10)

    cadastro_window.mainloop()