import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from conexao import connect_db

def exibir_ocupacoes(filtro=""):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        query = """
            SELECT o.cod_ocup, o.cod_vaga, o.cod_cliente, o.cod_veiculo, v.numero_vaga, c.nome_cliente, ve.placa
            FROM ocupacao o
            JOIN vagas v ON o.cod_vaga = v.cod_vaga
            JOIN clientes c ON o.cod_cliente = c.cod_cliente
            JOIN veiculos ve ON o.cod_veiculo = ve.cod_veiculo
        """

        if filtro:
            query += " WHERE o.cod_ocup LIKE %s OR o.cod_cliente LIKE %s OR o.cod_veiculo LIKE %s"
            cursor.execute(query, (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"))
        else:
            cursor.execute(query)

        ocupacoes = cursor.fetchall()
        conn.close()

        for item in tree.get_children():
            tree.delete(item)

        for ocupacao in ocupacoes:
            cod_ocup, cod_vaga, cod_cliente, cod_veiculo, numero_vaga, nome_cliente, placa = ocupacao
            tree.insert("", "end", values=(cod_ocup, numero_vaga, nome_cliente, placa))

def buscar_ocupacao():
    filtro = entry_busca.get()
    exibir_ocupacoes(filtro)

def ocupacao():
    global tree 

    window = tk.Tk()
    window.title("Ocupação do Estacionamento")

    tk.Label(window, text="Ocupação do Estacionamento").grid(row=0, columnspan=4)

    tk.Label(window, text="Buscar Ocupação (Código, Cliente ou Veículo):").grid(row=1, column=0, padx=10, pady=5)
    global entry_busca
    entry_busca = tk.Entry(window)
    entry_busca.grid(row=1, column=1, padx=10, pady=5)

    botao_busca = tk.Button(window, text="Buscar", command=buscar_ocupacao)
    botao_busca.grid(row=1, column=2, padx=10, pady=5)

    columns = ("Código da Ocupação", "Número da Vaga", "Nome do Cliente", "Placa do Veículo")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.grid(row=2, columnspan=4)

    for col in columns:
        tree.heading(col, text=col)

    exibir_ocupacoes()

    window.mainloop()