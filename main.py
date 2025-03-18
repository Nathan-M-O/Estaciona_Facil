import bcrypt
import tkinter as tk
from tkinter import messagebox
from conexao import connect_db
from cadastro import criar_tela_cadastro 

def iniciar_login():
    global login_window, entry_email, entry_senha  

    print("Iniciando a tela de login...")  

    login_window = tk.Tk()
    login_window.title("Tela de Login")

    tk.Label(login_window, text="Email").pack(pady=5)
    entry_email = tk.Entry(login_window)
    entry_email.pack(pady=5)

    tk.Label(login_window, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(login_window, show="*")
    entry_senha.pack(pady=5)

    tk.Button(login_window, text="Login", command=login_usuario).pack(pady=5)

    tk.Button(login_window, text="Cadastrar novo usuário", command=abrir_tela_cadastro).pack(pady=5)

    login_window.mainloop()  

def abrir_tela_cadastro():
    login_window.withdraw()  
    criar_tela_cadastro()  

def abrir_menu_principal():
    print("Login bem-sucedido! Abrindo menu principal...")  
    login_window.destroy()  
    root.deiconify()  

def login_usuario():
    global entry_email, entry_senha  
    
    email = entry_email.get()
    senha = entry_senha.get()

    if not email or not senha:
        messagebox.showerror("Erro", "Por favor, preencha o e-mail e a senha.")
        return

    print("Tentando realizar login...")  

    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
                messagebox.showinfo("Login", "Login realizado com sucesso!")
                abrir_menu_principal()  
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")

root = tk.Tk()
root.title("Menu Principal")
root.withdraw()  

print("Iniciando a tela de login...")  
iniciar_login()  