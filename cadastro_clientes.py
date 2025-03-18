import tkinter as tk
from tkinter import messagebox
from conexao import connect_db

def cadastrar_cliente(entry_nome_cliente, entry_email_cliente, entry_cpf_cliente, entry_telefone_cliente):
    nome = entry_nome_cliente.get()
    email = entry_email_cliente.get()
    cpf = entry_cpf_cliente.get()
    telefone = entry_telefone_cliente.get()

    if not nome or not email or not cpf or not telefone:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE cpf = %s", (cpf,))
        cliente = cursor.fetchone()

        if cliente:
            messagebox.showerror("Erro", "CPF já cadastrado.")
        else:
            cursor.execute("INSERT INTO clientes (nome, email, cpf, telefone) VALUES (%s, %s, %s, %s)", 
                           (nome, email, cpf, telefone))
            conn.commit()

            cliente_id = cursor.lastrowid
            messagebox.showinfo("Cadastro", "Cliente cadastrado com sucesso!")

            cadastrar_veiculo(cliente_id)
        
        cursor.close()
        conn.close()

def cadastrar_veiculo(cliente_id):
    def registrar_veiculo():
        placa = entry_placa.get()
        marca = entry_marca.get()
        modelo = entry_modelo.get()
        cor = entry_cor.get()

        if not placa or not marca or not modelo or not cor:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO veiculos (cliente_id, placa, marca, modelo, cor) VALUES (%s, %s, %s, %s, %s)", 
                           (cliente_id, placa, marca, modelo, cor))
            conn.commit()
            messagebox.showinfo("Cadastro", "Veículo cadastrado com sucesso!")
            cursor.close()
            conn.close()
            veiculo_window.destroy()  

    veiculo_window = tk.Tk()
    veiculo_window.title("Cadastro de Veículo")

    tk.Label(veiculo_window, text="Placa:").grid(row=0, column=0)
    tk.Label(veiculo_window, text="Marca:").grid(row=1, column=0)
    tk.Label(veiculo_window, text="Modelo:").grid(row=2, column=0)
    tk.Label(veiculo_window, text="Cor:").grid(row=3, column=0)

    entry_placa = tk.Entry(veiculo_window)
    entry_placa.grid(row=0, column=1)

    entry_marca = tk.Entry(veiculo_window)
    entry_marca.grid(row=1, column=1)

    entry_modelo = tk.Entry(veiculo_window)
    entry_modelo.grid(row=2, column=1)

    entry_cor = tk.Entry(veiculo_window)
    entry_cor.grid(row=3, column=1)

    tk.Button(veiculo_window, text="Cadastrar Veículo", command=registrar_veiculo).grid(row=4, column=0, columnspan=2)

    veiculo_window.mainloop()

def tela_cadastro_clientes():
    cadastro_cliente_window = tk.Tk()
    cadastro_cliente_window.title("Cadastro de Cliente")

    tk.Label(cadastro_cliente_window, text="Nome:").grid(row=0, column=0)
    tk.Label(cadastro_cliente_window, text="E-mail:").grid(row=1, column=0)
    tk.Label(cadastro_cliente_window, text="CPF:").grid(row=2, column=0)
    tk.Label(cadastro_cliente_window, text="Telefone:").grid(row=3, column=0)

    entry_nome_cliente = tk.Entry(cadastro_cliente_window)
    entry_nome_cliente.grid(row=0, column=1)

    entry_email_cliente = tk.Entry(cadastro_cliente_window)
    entry_email_cliente.grid(row=1, column=1)

    entry_cpf_cliente = tk.Entry(cadastro_cliente_window)
    entry_cpf_cliente.grid(row=2, column=1)

    entry_telefone_cliente = tk.Entry(cadastro_cliente_window)
    entry_telefone_cliente.grid(row=3, column=1)

    tk.Button(cadastro_cliente_window, text="Cadastrar Cliente", 
              command=lambda: cadastrar_cliente(entry_nome_cliente, entry_email_cliente, entry_cpf_cliente, entry_telefone_cliente)).grid(row=4, column=0, columnspan=2)

    cadastro_cliente_window.mainloop()