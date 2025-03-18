import tkinter as tk
from tkinter import messagebox
from conexao import connect_db
from enviar_email import enviar_email_recuperacao  

def verificar_email():
    email = entry_email_recuperacao.get()

    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            link_recuperacao = f"link_provisório{email}"
            enviar_email_recuperacao(email, link_recuperacao)
            messagebox.showinfo("Recuperação", f"Um link de recuperação foi enviado para {email}.")
            recuperacao_window.destroy()
        else:
            messagebox.showerror("Erro", "Este e-mail não está registrado.")

        cursor.close()
        conn.close()

def criar_tela_recuperacao():
    global recuperacao_window, entry_email_recuperacao

    recuperacao_window = tk.Toplevel()
    recuperacao_window.title("Recuperação de Senha")

    tk.Label(recuperacao_window, text="Digite seu e-mail").grid(row=0, column=0)

    entry_email_recuperacao = tk.Entry(recuperacao_window)
    entry_email_recuperacao.grid(row=0, column=1)

    tk.Button(recuperacao_window, text="Enviar link de recuperação", command=verificar_email).grid(row=1, column=0, columnspan=2)

def abrir_recuperacao_senha():
    criar_tela_recuperacao()