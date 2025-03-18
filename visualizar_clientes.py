import tkinter as tk
from tkinter import messagebox
from conexao import connect_db

def excluir_cliente(cliente_id):

    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        try:

            cursor.execute("DELETE FROM veiculos WHERE cliente_id = %s", (cliente_id,))

            cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao excluir cliente: {str(e)}")
        finally:
            cursor.close()
            conn.close()

def visualizar_clientes():

    visualizar_window = tk.Tk()
    visualizar_window.title("Visualizar Clientes e Veículos")

    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT c.id AS cliente_id, c.nome, c.email, c.cpf, c.telefone, v.placa, v.marca, v.modelo, v.cor
            FROM clientes c
            LEFT JOIN veiculos v ON c.id = v.cliente_id
        """)
        clientes = cursor.fetchall()

        if not clientes:
            messagebox.showinfo("Nenhum Cliente", "Não há clientes cadastrados.")
            return

        tk.Label(visualizar_window, text="ID Cliente").grid(row=0, column=0)
        tk.Label(visualizar_window, text="Nome").grid(row=0, column=1)
        tk.Label(visualizar_window, text="Email").grid(row=0, column=2)
        tk.Label(visualizar_window, text="CPF").grid(row=0, column=3)
        tk.Label(visualizar_window, text="Telefone").grid(row=0, column=4)
        tk.Label(visualizar_window, text="Placa").grid(row=0, column=5)
        tk.Label(visualizar_window, text="Marca").grid(row=0, column=6)
        tk.Label(visualizar_window, text="Modelo").grid(row=0, column=7)
        tk.Label(visualizar_window, text="Cor").grid(row=0, column=8)
        tk.Label(visualizar_window, text="Ações").grid(row=0, column=9)

        for idx, cliente in enumerate(clientes, start=1):
            tk.Label(visualizar_window, text=cliente['cliente_id']).grid(row=idx, column=0)
            tk.Label(visualizar_window, text=cliente['nome']).grid(row=idx, column=1)
            tk.Label(visualizar_window, text=cliente['email']).grid(row=idx, column=2)
            tk.Label(visualizar_window, text=cliente['cpf']).grid(row=idx, column=3)
            tk.Label(visualizar_window, text=cliente['telefone']).grid(row=idx, column=4)
            tk.Label(visualizar_window, text=cliente['placa'] if cliente['placa'] else "N/A").grid(row=idx, column=5)
            tk.Label(visualizar_window, text=cliente['marca'] if cliente['marca'] else "N/A").grid(row=idx, column=6)
            tk.Label(visualizar_window, text=cliente['modelo'] if cliente['modelo'] else "N/A").grid(row=idx, column=7)
            tk.Label(visualizar_window, text=cliente['cor'] if cliente['cor'] else "N/A").grid(row=idx, column=8)

            excluir_button = tk.Button(visualizar_window, text="Excluir", command=lambda cliente_id=cliente['cliente_id']: confirmar_exclusao(cliente_id, visualizar_window))
            excluir_button.grid(row=idx, column=9)

        cursor.close()
        conn.close()
        visualizar_window.mainloop()

def confirmar_exclusao(cliente_id, window):
    resposta = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir este cliente?")
    if resposta:
        excluir_cliente(cliente_id)
        window.destroy() 
        visualizar_clientes() 