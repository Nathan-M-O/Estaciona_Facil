import tkinter as tk
from tkinter import messagebox
from conexao import connect_db
import bcrypt 
from menu_principal import root 
from cadastro import criar_tela_cadastro  

def abrir_tela_cadastro():
    login_window.withdraw()  
    criar_tela_cadastro()  

def abrir_tela_recuperar_senha():
    recuperar_senha_window = tk.Toplevel(login_window)
    recuperar_senha_window.title("Recuperar Senha")
    
    tk.Label(recuperar_senha_window, text="Digite seu e-mail").pack(pady=5)
    entry_email_recuperar = tk.Entry(recuperar_senha_window)
    entry_email_recuperar.pack(pady=5)

    tk.Button(recuperar_senha_window, text="Recuperar", command=lambda: recuperar_senha(entry_email_recuperar.get())).pack(pady=5)

def recuperar_senha(email):
    if email:
        messagebox.showinfo("Recuperação de Senha", f"Um link de recuperação foi enviado para {email}.")
    else:
        messagebox.showerror("Erro", "Por favor, informe um e-mail válido.")

def login_usuario(entry_email, entry_senha, login_window):
    email = entry_email.get()
    senha = entry_senha.get()

    if not email or not senha:
        messagebox.showerror("Erro", "Por favor, preencha o e-mail e a senha.")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
                messagebox.showinfo("Login", "Login realizado com sucesso!")
                login_window.destroy() 
                abrir_menu_principal()  
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

        cursor.close()
        conn.close()

def abrir_menu_principal():
    root.deiconify()  

def iniciar_login():
    global login_window, entry_email, entry_senha 

    login_window = tk.Tk()
    login_window.title("Tela de Login")
    
    tk.Label(login_window, text="Email").pack(pady=5)
    entry_email = tk.Entry(login_window)
    entry_email.pack(pady=5)

    tk.Label(login_window, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(login_window, show="*")
    entry_senha.pack(pady=5)

    tk.Button(login_window, text="Login", command=lambda: login_usuario(entry_email, entry_senha, login_window)).pack(pady=5)

    tk.Button(login_window, text="Cadastrar novo usuário", command=abrir_tela_cadastro).pack(pady=5)

    tk.Button(login_window, text="Esqueci minha senha", command=abrir_tela_recuperar_senha).pack(pady=5)

    login_window.mainloop()

if __name__ == "__main__":
    iniciar_login()