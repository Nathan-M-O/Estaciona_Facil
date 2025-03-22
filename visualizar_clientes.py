import tkinter as tk
from tkinter import messagebox
from conexao import connect_db

def excluir_cliente(cod_cliente):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM veiculos WHERE cod_cliente = %s", (cod_cliente,))
            cursor.execute("DELETE FROM clientes WHERE cod_cliente = %s", (cod_cliente,))
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

    window_width = 920 
    window_height = 620  
    screen_width = visualizar_window.winfo_screenwidth()
    screen_height = visualizar_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    visualizar_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT c.cod_cliente AS cod_cliente, c.nome_cliente, c.email, c.cpf, c.telefone, 
                   v.placa, v.marca, v.modelo, v.cor, v.tipo_veiculo  -- Incluindo tipo_veiculo
            FROM clientes c
            LEFT JOIN veiculos v ON c.cod_cliente = v.cod_cliente
        """)
        clientes = cursor.fetchall()

        if not clientes:
            messagebox.showinfo("Nenhum Cliente", "Não há clientes cadastrados.")
            return

        font = ("Arial", 10)  

        tk.Label(visualizar_window, text="Código do Cliente", font=font).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(visualizar_window, text="Nome", font=font).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(visualizar_window, text="Email", font=font).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(visualizar_window, text="CPF", font=font).grid(row=0, column=3, padx=5, pady=5)
        tk.Label(visualizar_window, text="Telefone", font=font).grid(row=0, column=4, padx=5, pady=5)
        tk.Label(visualizar_window, text="Placa", font=font).grid(row=0, column=5, padx=5, pady=5)
        tk.Label(visualizar_window, text="Marca", font=font).grid(row=0, column=6, padx=5, pady=5)
        tk.Label(visualizar_window, text="Modelo", font=font).grid(row=0, column=7, padx=5, pady=5)
        tk.Label(visualizar_window, text="Cor", font=font).grid(row=0, column=8, padx=5, pady=5)
        tk.Label(visualizar_window, text="Tipo de Veículo", font=font).grid(row=0, column=9, padx=5, pady=5)  
        tk.Label(visualizar_window, text="Ações", font=font).grid(row=0, column=10, padx=5, pady=5)

        for idx, cliente in enumerate(clientes, start=1):
            tk.Label(visualizar_window, text=cliente['cod_cliente'], font=font).grid(row=idx, column=0, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['nome_cliente'], font=font).grid(row=idx, column=1, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['email'], font=font).grid(row=idx, column=2, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['cpf'], font=font).grid(row=idx, column=3, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['telefone'], font=font).grid(row=idx, column=4, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['placa'] if cliente['placa'] else "N/A", font=font).grid(row=idx, column=5, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['marca'] if cliente['marca'] else "N/A", font=font).grid(row=idx, column=6, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['modelo'] if cliente['modelo'] else "N/A", font=font).grid(row=idx, column=7, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['cor'] if cliente['cor'] else "N/A", font=font).grid(row=idx, column=8, padx=5, pady=5)
            tk.Label(visualizar_window, text=cliente['tipo_veiculo'] if cliente['tipo_veiculo'] else "N/A", font=font).grid(row=idx, column=9, padx=5, pady=5) 

            excluir_button = tk.Button(visualizar_window, text="Excluir", font=font, command=lambda cod_cliente=cliente['cod_cliente']: confirmar_exclusao(cod_cliente, visualizar_window))
            excluir_button.grid(row=idx, column=10, padx=5, pady=5)

        cursor.close()
        conn.close()
        visualizar_window.mainloop()

def confirmar_exclusao(cod_cliente, window):
    resposta = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir este cliente?")
    if resposta:
        excluir_cliente(cod_cliente)
        window.destroy()
        visualizar_clientes()