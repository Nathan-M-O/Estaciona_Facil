import tkinter as tk
from tkinter import messagebox
from conexao import connect_db
import bcrypt
from menu_principal import root
from cadastro import criar_tela_cadastro

def abrir_tela_cadastro():
    login_window.withdraw()  
    criar_tela_cadastro()  

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

    canvas = tk.Canvas(login_window, width=400, height=200, bg="white")
    canvas.grid(row=0, column=0, padx=20, pady=10) 

    canvas.create_rectangle(50, 100, 350, 150, fill="green", outline="black", width=2)
    canvas.create_rectangle(150, 50, 250, 100, fill="green", outline="black", width=2)
    canvas.create_oval(75, 140, 125, 190, fill="black")
    canvas.create_oval(275, 140, 325, 190, fill="black")

    tk.Label(login_window, text="Estaciona Fácil", font=("Arial", 24, "bold")).grid(row=1, column=0, pady=20)

    tk.Label(login_window, text="Email").grid(row=2, column=0, pady=10)
    entry_email = tk.Entry(login_window)
    entry_email.grid(row=3, column=0, pady=5)

    tk.Label(login_window, text="Senha").grid(row=4, column=0, pady=10)
    entry_senha = tk.Entry(login_window, show="*")
    entry_senha.grid(row=5, column=0, pady=5)

    tk.Button(login_window, text="Login", command=lambda: login_usuario(entry_email, entry_senha, login_window)).grid(row=6, column=0, pady=10)

    tk.Button(login_window, text="Cadastrar novo usuário", command=abrir_tela_cadastro).grid(row=7, column=0, pady=10)

    login_window.mainloop()

if __name__ == "__main__":
    iniciar_login()