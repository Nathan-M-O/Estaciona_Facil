import bcrypt
import tkinter as tk
from tkinter import messagebox
from conexao import connect_db
from cadastro import criar_tela_cadastro
from menu_principal import criar_menu_principal

def iniciar_login():
    global login_window, entry_email, entry_senha  

    print("Iniciando a tela de login...")  

    login_window = tk.Tk()
    login_window.title("Tela de Login")

    login_window.state('zoomed')

    tk.Label(login_window, text="Email", font=("Arial", 14)).pack(pady=20)
    entry_email = tk.Entry(login_window, font=("Arial", 14), width=30)
    entry_email.pack(pady=10)

    tk.Label(login_window, text="Senha", font=("Arial", 14)).pack(pady=20)
    entry_senha = tk.Entry(login_window, show="*", font=("Arial", 14), width=30)
    entry_senha.pack(pady=10)

    tk.Button(login_window, text="Login", command=login_usuario, font=("Arial", 14), width=20, height=2).pack(pady=20)
    tk.Button(login_window, text="Cadastrar novo usuário", command=abrir_tela_cadastro, font=("Arial", 14), width=20, height=2).pack(pady=10)

    login_window.mainloop()  

def abrir_tela_cadastro():
    criar_tela_cadastro(login_window)   

def abrir_menu_principal():
    print("Login bem-sucedido! Abrindo menu principal...")
    login_window.withdraw() 
    root = tk.Tk()  
    criar_menu_principal(root)  
    root.state('zoomed') 
    root.mainloop()

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

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")

    finally:
        if conn:  
            conn.close()  

print("Iniciando a tela de login...")  
iniciar_login()