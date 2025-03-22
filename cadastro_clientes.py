import tkinter as tk
from tkinter import messagebox
from conexao import connect_db

def cadastrar_cliente(entry_nome_cliente, entry_email_cliente, entry_cpf_cliente, entry_telefone_cliente, cadastro_cliente_window, menu_principal_window):
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
            cursor.execute("INSERT INTO clientes (nome_cliente, email, cpf, telefone) VALUES (%s, %s, %s, %s)", 
                           (nome, email, cpf, telefone))
            conn.commit()

            cliente_id = cursor.lastrowid 
            messagebox.showinfo("Cadastro", "Cliente cadastrado com sucesso!")

            cadastro_cliente_window.withdraw() 

            cadastrar_veiculo(cliente_id, menu_principal_window)
        
        cursor.close()
        conn.close()

def cadastrar_veiculo(cliente_id, menu_principal_window):
    def registrar_veiculo():
        placa = entry_placa.get()
        marca = entry_marca.get()
        modelo = entry_modelo.get()
        cor = entry_cor.get()
        tipo = entry_tipo_veiculo.get()  

        if not placa or not marca or not modelo or not cor or not tipo: 
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO veiculos (cod_cliente, placa, marca, modelo, cor, tipo_veiculo) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (cliente_id, placa, marca, modelo, cor, tipo))
            conn.commit()
            messagebox.showinfo("Cadastro", "Veículo cadastrado com sucesso!")

            cursor.close()
            conn.close()

            veiculo_window.destroy()

            menu_principal_window.deiconify()

    veiculo_window = tk.Tk()
    veiculo_window.title("Cadastro de Veículo")
    veiculo_window.geometry("800x600")  

    tk.Label(veiculo_window, text="Placa:", font=("Arial", 14)).grid(row=0, column=0, pady=10)
    tk.Label(veiculo_window, text="Marca:", font=("Arial", 14)).grid(row=1, column=0, pady=10)
    tk.Label(veiculo_window, text="Modelo:", font=("Arial", 14)).grid(row=2, column=0, pady=10)
    tk.Label(veiculo_window, text="Cor:", font=("Arial", 14)).grid(row=3, column=0, pady=10)
    tk.Label(veiculo_window, text="Tipo de Veículo:", font=("Arial", 14)).grid(row=4, column=0, pady=10)

    entry_placa = tk.Entry(veiculo_window, font=("Arial", 14), width=30)
    entry_placa.grid(row=0, column=1, padx=10, pady=10)

    entry_marca = tk.Entry(veiculo_window, font=("Arial", 14), width=30)
    entry_marca.grid(row=1, column=1, padx=10, pady=10)

    entry_modelo = tk.Entry(veiculo_window, font=("Arial", 14), width=30)
    entry_modelo.grid(row=2, column=1, padx=10, pady=10)

    entry_cor = tk.Entry(veiculo_window, font=("Arial", 14), width=30)
    entry_cor.grid(row=3, column=1, padx=10, pady=10)

    entry_tipo_veiculo = tk.Entry(veiculo_window, font=("Arial", 14), width=30)
    entry_tipo_veiculo.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(veiculo_window, text="Cadastrar Veículo", command=registrar_veiculo, font=("Arial", 14), width=20, height=2).grid(row=5, column=0, columnspan=2, pady=20)

    veiculo_window.mainloop()

def tela_cadastro_clientes(menu_principal_window):
    cadastro_cliente_window = tk.Tk()
    cadastro_cliente_window.title("Cadastro de Cliente")
    cadastro_cliente_window.geometry("800x600")  

    
    tk.Label(cadastro_cliente_window, text="Nome:", font=("Arial", 14)).grid(row=0, column=0, pady=10)
    tk.Label(cadastro_cliente_window, text="E-mail:", font=("Arial", 14)).grid(row=1, column=0, pady=10)
    tk.Label(cadastro_cliente_window, text="CPF:", font=("Arial", 14)).grid(row=2, column=0, pady=10)
    tk.Label(cadastro_cliente_window, text="Telefone:", font=("Arial", 14)).grid(row=3, column=0, pady=10)

    entry_nome_cliente = tk.Entry(cadastro_cliente_window, font=("Arial", 14), width=30)
    entry_nome_cliente.grid(row=0, column=1, padx=10, pady=10)

    entry_email_cliente = tk.Entry(cadastro_cliente_window, font=("Arial", 14), width=30)
    entry_email_cliente.grid(row=1, column=1, padx=10, pady=10)

    entry_cpf_cliente = tk.Entry(cadastro_cliente_window, font=("Arial", 14), width=30)
    entry_cpf_cliente.grid(row=2, column=1, padx=10, pady=10)

    entry_telefone_cliente = tk.Entry(cadastro_cliente_window, font=("Arial", 14), width=30)
    entry_telefone_cliente.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(cadastro_cliente_window, text="Cadastrar Cliente", 
              command=lambda: cadastrar_cliente(entry_nome_cliente, entry_email_cliente, entry_cpf_cliente, entry_telefone_cliente, cadastro_cliente_window, menu_principal_window), 
              font=("Arial", 14), width=20, height=2).grid(row=4, column=0, columnspan=2, pady=20)

    cadastro_cliente_window.mainloop()