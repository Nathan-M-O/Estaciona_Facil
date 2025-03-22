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

def excluir_ocupacao(window):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma ocupação para excluir!")
        return

    cod_ocup = tree.item(selected_item, 'values')[0] 

    if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a ocupação {cod_ocup}?"):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT cod_vaga
                FROM ocupacao
                WHERE cod_ocup = %s
            """, (cod_ocup,))
            vaga = cursor.fetchone()

            if vaga:
                cod_vaga = vaga[0]

                cursor.execute("""
                    SELECT numero_vaga
                    FROM vagas
                    WHERE cod_vaga = %s
                """, (cod_vaga,))
                numero_vaga = cursor.fetchone()

                if numero_vaga:
                    cursor.execute("DELETE FROM ocupacao WHERE cod_ocup = %s", (cod_ocup,))

                    cursor.execute("UPDATE vagas SET disponibilidade = 0 WHERE cod_vaga = %s", (cod_vaga,))
                    conn.commit() 

                    messagebox.showinfo("Sucesso", "Ocupação excluída com sucesso!")
                else:
                    messagebox.showerror("Erro", "Falha ao encontrar o número da vaga associada à ocupação.")
            else:
                messagebox.showerror("Erro", "Falha ao encontrar a vaga associada à ocupação.")

            conn.close()
            exibir_ocupacoes() 
            window.destroy()  
        else:
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados.")

def ocupar_vaga(window):
    numero_vaga = entry_vaga.get()  
    cod_cliente = entry_cliente.get()

    if not numero_vaga or not cod_cliente:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v.cod_vaga, v.disponibilidade 
            FROM vagas v
            WHERE v.numero_vaga = %s
        """, (numero_vaga,))
        vaga = cursor.fetchone()

        if not vaga:
            messagebox.showerror("Erro", "Vaga não encontrada!")
            conn.close()
            return

        if vaga[1] == 1:
            messagebox.showerror("Erro", "Vaga já está ocupada!")
            conn.close()
            return

        cursor.execute("SELECT cod_veiculo FROM veiculos WHERE cod_cliente = %s", (cod_cliente,))
        veiculo = cursor.fetchone()

        if not veiculo:
            messagebox.showerror("Erro", "Cliente não possui veículo cadastrado!")
            conn.close()
            return

        cod_veiculo = veiculo[0]

        cursor.execute(""" 
            INSERT INTO ocupacao (cod_vaga, cod_cliente, cod_veiculo)
            VALUES (%s, %s, %s)
        """, (vaga[0], cod_cliente, cod_veiculo))  

        cursor.execute("UPDATE vagas SET disponibilidade = 1 WHERE cod_vaga = %s", (vaga[0],))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Vaga ocupada com sucesso!")
        exibir_ocupacoes() 
        window.destroy()  

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

    tk.Label(window, text="Código da Vaga:").grid(row=2, column=0, padx=10, pady=5)
    global entry_vaga
    entry_vaga = tk.Entry(window)
    entry_vaga.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(window, text="Código do Cliente:").grid(row=3, column=0, padx=10, pady=5)
    global entry_cliente
    entry_cliente = tk.Entry(window)
    entry_cliente.grid(row=3, column=1, padx=10, pady=5)

    botao_ocupar = tk.Button(window, text="Ocupar Vaga", command=lambda: ocupar_vaga(window))
    botao_ocupar.grid(row=3, column=2, padx=10, pady=5)

    botao_excluir = tk.Button(window, text="Excluir Ocupação", command=lambda: excluir_ocupacao(window))
    botao_excluir.grid(row=5, column=0, columnspan=4, pady=10)

    columns = ("Código da Ocupação", "Número da Vaga", "Nome do Cliente", "Placa do Veículo")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.grid(row=4, columnspan=4)

    for col in columns:
        tree.heading(col, text=col)

    exibir_ocupacoes()

    window.mainloop()